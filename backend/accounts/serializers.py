from .models import Account, JoinedRequest
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class AccountSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField()
    has_read_access = serializers.SerializerMethodField()
    has_write_access = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = (
            "id",
            "account_type",
            "conf_label",
            "integrity_label",
            "amount",
            "user",
            "username",
            "has_read_access",
            "has_write_access",
            "created_at",
            "updated_at",
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
