import re

from django.core.exceptions import ValidationError


# ? setFullName
def setFullName(name: str, surname: str) -> str:
    return f"{name} {surname}"


# ? setPetName
def setPetName(name: str) -> str:
    return f"{name}"


# ? is_valid_wallet_address
def is_valid_wallet_address(wallet_address: str):
    pattern = r"^0x[a-fA-F0-9]{40}$"
    if wallet_address == "" or wallet_address is None:
        return ""
    elif not re.match(pattern, wallet_address):
        raise ValidationError("Invalid MetaMask address.")
    return True
