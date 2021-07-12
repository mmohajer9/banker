from .models import Account, AuditLog, JoinedRequest, Transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db.models import F


class JoinedRequestSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField()
    requested_account_owner = serializers.SerializerMethodField()

    class Meta:
        model = JoinedRequest
        fields = (
            "id",
            "user",
            "username",
            "requested_account",
            "requested_account_owner",
            "conf_label",
            "integrity_label",
            "status",
            "created_at",
            "updated_at",
            "has_read_access",
            "has_write_access",
        )

    def get_username(self, obj):
        return obj.user.username

    def get_requested_account_owner(self, obj):
        return obj.requested_account.user.username


class JoinedRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinedRequest
        fields = ("requested_account",)

    def create(self, validated_data):

        user = validated_data.get("user")
        requested_account = validated_data.get("requested_account")

        if user == requested_account.user:
            raise ValidationError({"error": _("You can not request to yourself")})

        if JoinedRequest.objects.filter(
            user=user, requested_account=requested_account
        ).exists():
            raise ValidationError(
                {"error": _("You can not request to this account twice")}
            )

        return super().create(validated_data)


class JoinedRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinedRequest
        fields = (
            "user",
            "requested_account",
            "conf_label",
            "integrity_label",
            "status",
        )
        read_only_fields = ["user", "requested_account"]


class TransactionSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = (
            "id",
            # "user",
            "username",
            "transaction_type",
            "amount",
            "from_account",
            "to_account",
        )

    def validate(self, attrs):

        instance = Transaction(**attrs)
        instance.full_clean()

        return super().validate(attrs)

    def create(self, validated_data):
        request = self.context.get("request", None)
        user = validated_data.get("user")
        transaction_type = validated_data.get("transaction_type")
        from_account = validated_data.get("from_account")
        to_account = validated_data.get("to_account")
        amount = validated_data.get("amount")

        if transaction_type == "deposit":
            Account.objects.filter(id=to_account.id).update(amount=F("amount") + amount)

        elif transaction_type == "withdraw":

            joined_request = JoinedRequest.objects.filter(
                user=user,
                requested_account=from_account,
                status="accepted",
            )
            if joined_request.exists():
                if not joined_request.first().has_write_access():
                    AuditLog.objects.create(
                        action="Access Control : No Write Access",
                        path=request.path,
                        method=request.method,
                        user=request.user,
                        remote_address=request.META.get("REMOTE_ADDR"),
                        content_type=request.META.get("CONTENT_TYPE"),
                        log_name=request.META.get("LOGNAME"),
                        browser=request.META.get("BROWSER"),
                        user_agent=request.META.get("HTTP_USER_AGENT"),
                    )
                    raise ValidationError(
                        {
                            "user": _(
                                "This user does not have access to the source account because of low access level"
                            )
                        }
                    )
            else:
                if not from_account.user == user:
                    AuditLog.objects.create(
                        action="Access Control : No Write Access",
                        path=request.path,
                        method=request.method,
                        user=request.user,
                        remote_address=request.META.get("REMOTE_ADDR"),
                        content_type=request.META.get("CONTENT_TYPE"),
                        log_name=request.META.get("LOGNAME"),
                        browser=request.META.get("BROWSER"),
                        user_agent=request.META.get("HTTP_USER_AGENT"),
                    )
                    raise ValidationError(
                        {
                            "user": _(
                                "This user does not have access to the source account because of low access level"
                            )
                        }
                    )

            Account.objects.filter(id=from_account.id).update(
                amount=F("amount") - amount
            )
            Account.objects.filter(id=to_account.id).update(amount=F("amount") + amount)

        return super().create(validated_data)

    def get_username(self, obj):
        return obj.user.username


class AccountSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField()
    has_read_access = serializers.SerializerMethodField()
    has_write_access = serializers.SerializerMethodField()
    transactions_as_sender = TransactionSerializer(many=True, read_only=True)
    transactions_as_reciever = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = (
            "id",
            "account_type",
            "conf_label",
            "integrity_label",
            "amount",
            # "user",
            "username",
            "has_read_access",
            "has_write_access",
            "created_at",
            "updated_at",
            "transactions_as_sender",
            "transactions_as_reciever",
        )

    def get_username(self, obj):
        return obj.user.username

    def get_has_read_access(self, obj):
        user = self.context["request"].user

        try:
            jr = JoinedRequest.objects.get(
                user=user,
                requested_account=obj,
                status="accepted",
            )

            return jr.has_read_access()
        except:
            return True

    def get_has_write_access(self, obj):
        user = self.context["request"].user
        try:
            jr = JoinedRequest.objects.get(
                user=user,
                requested_account=obj,
                status="accepted",
            )

            return jr.has_write_access()
        except:
            return True
