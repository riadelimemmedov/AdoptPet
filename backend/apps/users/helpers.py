from django.contrib.auth import get_user_model

# User
User = get_user_model()


# ?is_exists_wallet_address
def is_exists_wallet_address(wallet_address: str):
    if User.objects.filter(wallet_address=wallet_address).exists():
        return True
    return False
