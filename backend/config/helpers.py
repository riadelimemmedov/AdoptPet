import re

from django.core.cache import cache
from django.core.exceptions import ValidationError
from eth_utils import keccak, to_checksum_address
from faker import Faker

# faker instance
faker = Faker()


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
        return ValidationError("Please enter a wallet address")
    elif not re.match(pattern, wallet_address):
        raise ValidationError("Invalid MetaMask wallet address address.")
    return True


# ?show_toolbar
def show_toolbar(request):
    return True


# ?check_cache
def clear_cache_put(cache_key: str):
    cache.delete(cache_key)


# ?generate_metamask_address
def generate_metamask_address():
    fake = Faker()
    private_key = fake.sha256()  # Generate a random private key
    public_key = keccak(bytes.fromhex(private_key[2:]))[-20:]  # Generate the public key
    address = to_checksum_address(public_key.hex())
    return address


# ?append_trailing_slash
def append_trailing_slash(url):
    return url if url[-1] == "/" else url + "/"


# ? generate_session_id
def generate_session_id() -> str:
    random_letters = faker.random_letters(length=30)
    value = "cs_test_{}".format("".join(random_letters))
    return value
