from .models import Account, JoinedRequest
from rest_framework import serializers


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


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("amount",)
