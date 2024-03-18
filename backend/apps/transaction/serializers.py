import re

from rest_framework import serializers

from .models import Transaction
from .validate_field import validate_confirmations, validate_from_user


# !TransactionSerializer
class TransactionSerializer(serializers.ModelSerializer):
    from_user = serializers.CharField(validators=[validate_from_user])
    confirmations = serializers.CharField(validators=[validate_confirmations])

    def validate(self, attrs):
        from_user = attrs.get("from_user")
        confirmations = attrs.get("confirmations")

        if not validate_from_user(from_user):
            raise serializers.ValidationError("Please input valid wallet address")
        if not validate_confirmations(confirmations):
            raise serializers.ValidationError("Confirmations value 1 or 0")
        return attrs

    class Meta:
        model = Transaction
        fields = "__all__"
