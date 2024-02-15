import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from config.helpers import is_valid_wallet_address

# *If you don't declare pytestmark our test class model don't accsess to database table
pytestmark = pytest.mark.django_db


# !TestUsersManagers
class TestUsersManagers:

    def test_str_method(self, user_factory):
        user = user_factory.create_user(email="normal_user@gmail.com", password="foo")
        assert user.__str__() == "normal_user@gmail.com"

    def test_valid_wallet_address(self):
        address = "0xCeD6ADEbbdDB8fE9AC85C359EbB5BEe0c03F67C2"
        assert is_valid_wallet_address(address) is True

    def test_invalid_metamask_address(self):
        address = "0xCetyythda7788aX"
        with pytest.raises(ValidationError):
            is_valid_wallet_address(address)

    def test_empty_wallet_address(self):
        address = ""
        assert is_valid_wallet_address(address) == ""

    def test_create_user(self, user_factory):
        user = user_factory.create_user(email="normal_user@gmail.com", password="foo")
        assert user.email == "normal_user@gmail.com"
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            assert user.username is None
        except (
            AttributeError
        ):  # Raised when an attribute reference (see Attribute references) or assignment fails
            pass

    def test_create_superuser(self, user_factory):
        admin_user = user_factory.create_superuser(
            email="super_user@gmail.com",
            password="foo",
            is_superuser=True,
            is_staff=True,
        )
        assert admin_user.email == "super_user@gmail.com"
        assert admin_user.is_active is True
        assert admin_user.is_staff is True
        assert admin_user.is_superuser is True
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            assert admin_user.username is None
        except (
            AttributeError
        ):  # Raised when an attribute reference (see Attribute references) or assignment fails
            pass
        with pytest.raises(ValueError):
            user_factory.create_superuser(
                email="super_user@gmail.com",
                password="foo",
                is_superuser=False,
                is_staff=False,
            )
