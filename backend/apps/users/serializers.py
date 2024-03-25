from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.transaction.validate_field import (
    validate_confirmations,
    validate_wallet_address,
)

from .helpers import is_exists_wallet_address
from .models import CustomUser


# !CustomUserSerializer
class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize CustomUser model.
    """

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "wallet_address")


# !UserRegisterationSerializer
class UserRegisterationSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize registration requests and create a new user.
    """

    wallet_address = serializers.CharField(validators=[validate_wallet_address])

    def validate_wallet_address(self, wallet_address):
        if not validate_wallet_address(wallet_address):
            raise serializers.ValidationError("Please input valid wallet address")
        elif is_exists_wallet_address(wallet_address):
            raise serializers.ValidationError("This wallet address already set other")
        return wallet_address

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "password", "wallet_address")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


# !UserLoginSerializer
class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users with email and password.
    """

    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
