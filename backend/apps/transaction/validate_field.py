import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


# ?validate_confirmations
def validate_confirmations(value):
    if int(value) > 1:
        return False
    return value


# ?validate_wallet_address
def validate_wallet_address(value):
    pattern = re.compile("^0x[a-fA-F0-9]{40}$")
    return bool(pattern.match(f"{value}"))
