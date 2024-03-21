import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from abstract.constants import PaymentOptions
from apps.transaction.models import Transaction
from apps.user_profile.models import Profile

# *If you don't declare pytestmark our test class model don't accsess to database table
pytestmark = pytest.mark.django_db


# !TestTransactionManagers
class TestTransactionManagers:
    def check_length(self, transaction_dict):
        """
        Check the length of various fields in a transaction dictionary and determine if they exceed the allowed limits.

        Args:
            transaction_dict (dict): A dictionary containing transaction details.

        Returns:
            bool: True if all field lengths are within the allowed limits, False otherwise.

        Raises:
            None.

        Example:
            transaction = {
                "from_user": "john_doe",
                "confirmations": 3,
                "value": "100.50",
                "adopted_pet_slug": "cute_kitten_001",
                "payment_options": "credit_card",
                "session_id": "abc123xyz789",
            }
            if check_length(transaction):
                print("All field lengths are within the allowed limits.")
            else:
                print("One or more field lengths exceed the allowed limits.")
        """
        if (
            len(transaction_dict["from_user"]) > 10
            or transaction_dict["confirmations"] > 1
            or len(transaction_dict["value"]) > 100
            or len(transaction_dict["adopted_pet_slug"]) > 100
            or len(transaction_dict["payment_options"]) > 100
            or len(transaction_dict["session_id"]) > 100
        ):
            return False
        return True

    def test_str_method(self, transaction_factory):
        """
        Test the __str__() method of the Transaction object.

        Args:
            self: The test case instance.
            transaction_factory (function): A factory function that generates Transaction objects.

        Returns:
            None.

        Raises:
            AssertionError: If the __str__() method does not produce the expected output.

        Example:
            transaction = Transaction(from_user="john_doe", value="100.50", payment_options="credit_card")
            test_str_method(self, lambda: transaction)
        """
        obj = transaction_factory()
        assert (
            obj.__str__() == f"{obj.from_user} -- {obj.value} -- {obj.payment_options}"
        )

    def test_max_length_method(self, transaction_factory):
        """
        Test the max length validation and cleaning of Transaction object fields.

        Args:
            self: The test case instance.
            transaction_factory (function): A factory function that generates Transaction objects.

        Returns:
            None.

        Raises:
            AssertionError: If the max length validation or cleaning results in unexpected behavior.
            ValidationError: If the max length validation fails.

        Example:
            def transaction_factory():
                return Transaction()

            test_max_length_method(self, transaction_factory)
        """
        from_user = "x" * 150
        confirmations = 2
        value = "y" * 150
        adopted_pet_slug = "z" * 150
        payment_options = "d" * 150
        session_id = "e" * 150
        is_checked_length = self.check_length(
            {
                "from_user": from_user,
                "confirmations": confirmations,
                "value": value,
                "adopted_pet_slug": adopted_pet_slug,
                "payment_options": payment_options,
                "session_id": session_id,
            }
        )
        obj = Transaction.objects.create(
            from_user=from_user,
            confirmations=confirmations,
            value=value,
            adopted_pet_slug=adopted_pet_slug,
            payment_options=payment_options,
            session_id=session_id,
        )
        if not is_checked_length:
            with pytest.raises(ValidationError):
                obj.full_clean()
        else:
            assert obj.full_clean() is None
            assert len(from_user) <= 100
            assert confirmations <= 1
            assert len(value) <= 100
            assert len(adopted_pet_slug) <= 100
            assert len(payment_options) <= 100
            assert len(session_id) <= 100

    def test_check_length(self, transaction_factory):
        """
        Test the length constraints of fields in a Transaction object.

        Args:
            self: The test case instance.
            transaction_factory (function): A factory function that generates Transaction objects.

        Returns:
            None.

        Raises:
            AssertionError: If any field length exceeds the allowed limit.

        Example:
            def transaction_factory():
                return Transaction()

            test_check_length(self, transaction_factory)
        """
        obj = transaction_factory()
        assert len(obj.from_user) <= 100
        assert obj.confirmations <= 1
        assert len(obj.value) <= 100
        assert len(obj.adopted_pet_slug) <= 100
        assert len(obj.payment_options) <= 100
        assert len(obj.session_id) <= 100

    def test_adopted_pet_slug(self, transaction_factory):
        """
        Test the properties of the 'adopted_pet_slug' field in a Transaction object.

        Args:
            self: The test case instance.
            transaction_factory (function): A factory function that generates Transaction objects.

        Returns:
            None.

        Raises:
            AssertionError: If any property of the 'adopted_pet_slug' field is not as expected.

        Example:
            def transaction_factory():
                return Transaction()

            test_adopted_pet_slug(self, transaction_factory)
        """
        obj = transaction_factory()
        adopted_pet_slug = obj._meta.get_field("adopted_pet_slug")
        assert adopted_pet_slug.max_length <= 100
        assert adopted_pet_slug.unique is True
        assert adopted_pet_slug.blank is False
        assert adopted_pet_slug.db_index is True

    def test_payment_options(self, transaction_factory):
        """
        Test the validity of the 'payment_options' field in a Transaction object.

        Args:
            self: The test case instance.
            transaction_factory (function): A factory function that generates Transaction objects.

        Returns:
            None.

        Raises:
            AssertionError: If the 'payment_options' field value is not found in the PaymentOptions enum.

        Example:
            def transaction_factory():
                return Transaction()

            test_payment_options(self, transaction_factory)
        """
        obj = transaction_factory()
        assert (
            any(option[0] == obj.payment_options for option in PaymentOptions)
        ) is True

    def test_session_id(self, transaction_factory):
        """
        Test the format of the 'session_id' field in a Transaction object.

        Args:
            self: The test case instance.
            transaction_factory (function): A factory function that generates Transaction objects.

        Returns:
            None.

        Raises:
            AssertionError: If the 'session_id' field value does not start with "cs_test_".

        Example:
            def transaction_factory():
                return Transaction()

            test_session_id(self, transaction_factory)
        """
        obj = transaction_factory()
        assert obj.session_id.startswith("cs_test_") is True

    def test_from_user_is_lowercase(self, transaction_factory):
        """
        Test if the 'from_user' field value in a Transaction object is lowercase.

        Args:
            self: The test case instance.
            transaction_factory (function): A factory function that generates Transaction objects.

        Returns:
            None.

        Raises:
            AssertionError: If the 'from_user' field value contains uppercase characters.

        Example:
            def transaction_factory():
                return Transaction()

            test_from_user_is_lowercase(self, transaction_factory)
        """
        obj = transaction_factory()
        assert obj.from_user.islower() is True
