import re

from rest_framework import serializers

from .models import Transaction
from .validate_field import validate_confirmations, validate_wallet_address


# !TransactionSerializer
class TransactionSerializer(serializers.ModelSerializer):
    from_user = serializers.CharField(validators=[validate_wallet_address])
    confirmations = serializers.CharField(validators=[validate_confirmations])

    def validate(self, attrs):
        from_user = attrs.get("from_user")
        confirmations = attrs.get("confirmations")

        if not validate_wallet_address(from_user):
            raise serializers.ValidationError("Please input valid wallet address")
        if not validate_confirmations(confirmations):
            raise serializers.ValidationError("Confirmations value 1 or 0")
        return attrs

    class Meta:
        model = Transaction
        fields = "__all__"
