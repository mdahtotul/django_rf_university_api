from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import User


class LoginSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField("get_tokens")

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "role",
            "avatar",
            "tokens",
        ]

    def get_tokens(self, instance):
        refresh = RefreshToken.for_user(instance)
        refresh["role"] = instance.role

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "avatar",
        ]
