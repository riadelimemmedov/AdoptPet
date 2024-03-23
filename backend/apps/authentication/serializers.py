from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from apps.users.models import CustomUser


class CustomRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = "__all__"

    def validate(self, attrs):
        username = attrs.get("username")
        email = attrs.get("email")
        if not username:
            raise serializers.ValidationError(("Username is required."))

        if not email:
            raise serializers.ValidationError(("Email is required."))

        return attrs
