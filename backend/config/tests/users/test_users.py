import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from config.helpers import is_valid_wallet_address

# *If you don't declare pytestmark our test class model don't accsess to database table
pytestmark = pytest.mark.django_db


# !TestUsersManagers
class TestUsersManagers:

    def test_str_method(self, user_factory):
        """
        Test the __str__ method of the user object.

        Args:
            user_factory: A factory function or object used to create a user object.

        Returns:
            None

        Example usage:
            test_str_method(user_factory)

        This method tests the __str__ method of the user object to ensure that it returns the expected string representation.

        The method performs the following steps:
        1. Creates a user object using the user_factory and assigns it to the `user` variable. The email is set to "normal_user@gmail.com" and the password is set to "foo".
        2. Asserts that the result of calling the __str__ method on the user object is equal to "normal_user@gmail.com".

        If the assertion passes, the test is considered successful. If the assertion fails, the test fails.
        """
        user = user_factory.create_user(email="normal_user@gmail.com", password="foo")
        assert user.__str__() == "normal_user@gmail.com"

    def test_valid_wallet_address(self):
        """
        Test the is_valid_wallet_address function.

        Returns:
            None

        Example usage:
            test_valid_wallet_address()

        This method tests the is_valid_wallet_address function to ensure that it correctly validates a wallet address.

        The method performs the following steps:
        1. Assigns a sample wallet address to the `address` variable.
        2. Calls the is_valid_wallet_address function with the `address` variable as an argument.
        3. Asserts that the result of the is_valid_wallet_address function is True.

        If the assertion passes, the test is considered successful. If the assertion fails, the test fails.
        """
        address = "0xCeD6ADEbbdDB8fE9AC85C359EbB5BEe0c03F67C2"
        assert is_valid_wallet_address(address) is True

    def test_invalid_metamask_address(self):
        """
        Test the is_valid_wallet_address function with an invalid MetaMask address.

        Returns:
            None

        Example usage:
            test_invalid_metamask_address()

        This method tests the is_valid_wallet_address function to ensure that it correctly detects an invalid MetaMask address.

        The method performs the following steps:
        1. Assigns an invalid MetaMask address to the `address` variable.
        2. Uses pytest.raises context manager to assert that a ValidationError is raised when calling the is_valid_wallet_address function with the `address`.

        If the ValidationError is raised, the test is considered successful. If a different exception is raised or no exception is raised, the test fails.
        """
        address = "0xCetyythda7788aX"
        with pytest.raises(ValidationError):
            is_valid_wallet_address(address)

    def test_empty_wallet_address(self):
        """
        Test the is_valid_wallet_address function with an empty wallet address.

        Returns:
            None

        Example usage:
            test_empty_wallet_address()

        This method tests the is_valid_wallet_address function to ensure that it correctly handles an empty wallet address.

        The method performs the following steps:
        1. Assigns an empty string to the `address` variable.
        2. Calls the is_valid_wallet_address function with the `address` variable as an argument.
        3. Asserts that the result of the is_valid_wallet_address function is an empty string.

        If the assertion passes, the test is considered successful. If the assertion fails, the test fails.
        """
        address = ""
        assert is_valid_wallet_address(address) == ""

    def test_create_user(self, user_factory):
        """
        Test the create_user method of the user_factory.

        Args:
            user_factory: A factory function or object used to create a user object.

        Returns:
            None

        Example usage:
            test_create_user(user_factory)

        This method tests the create_user method of the user_factory to ensure that it correctly creates a user object with the specified email and password.

        The method performs the following steps:
        1. Calls the create_user method of the user_factory with the email set to "normal_user@gmail.com" and the password set to "foo". Assigns the resulting user object to the `user` variable.
        2. Asserts that the email property of the user object is equal to "normal_user@gmail.com".
        3. Asserts that the is_active property of the user object is True.
        4. Asserts that the is_staff property of the user object is False.
        5. Asserts that the is_superuser property of the user object is False.
        6. Uses a try-except block to handle cases where the username property does not exist (e.g., when using AbstractUser or AbstractBaseUser options). Inside the try block, asserts that the username property of the user object is None.
        7. If an AttributeError is raised during the assertion, the pass statement is executed to handle it.

        If all the assertions pass, the test is considered successful. If any of the assertions fail or an unexpected exception is raised, the test fails.

        """
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
        """
        Test the create_superuser method of the user_factory.

        Args:
            user_factory: A factory function or object used to create a user object.

        Returns:
            None

        Example usage:
            test_create_superuser(user_factory)

        This method tests the create_superuser method of the user_factory to ensure that it correctly creates a superuser object with the specified email, password, is_superuser, and is_staff values.

        The method performs the following steps:
        1. Calls the create_superuser method of the user_factory with the email set to "super_user@gmail.com", the password set to "foo", is_superuser set to True, and is_staff set to True. Assigns the resulting superuser object to the `admin_user` variable.
        2. Asserts that the email property of the admin_user object is equal to "super_user@gmail.com".
        3. Asserts that the is_active property of the admin_user object is True.
        4. Asserts that the is_staff property of the admin_user object is True.
        5. Asserts that the is_superuser property of the admin_user object is True.
        6. Uses a try-except block to handle cases where the username property does not exist (e.g., when using AbstractUser or AbstractBaseUser options). Inside the try block, asserts that the username property of the admin_user object is None.
        7. If an AttributeError is raised during the assertion, the pass statement is executed to handle it.
        8. Uses pytest.raises context manager to assert that a ValueError is raised when calling the create_superuser method of the user_factory with is_superuser set to False and is_staff set to False.

        If all the assertions pass and the ValueError is raised as expected, the test is considered successful. If any of the assertions fail or an unexpected exception is raised, the test fails.

        """
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
