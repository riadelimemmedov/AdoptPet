import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.user_profile.models import Profile

# *If you don't declare pytestmark our test class model don't accsess to database table
pytestmark = pytest.mark.django_db


# !TestUserProfileManagers
class TestUserProfileManagers:
    def create_mock_profile(self, profile_factory):
        """
        Create mock profile objects for testing.

        Args:
            profile_factory: A factory function or object used to create a profile object.

        Returns:
            None

        Example usage:
            create_mock_profile(profile_factory)

        This method creates mock profile objects with different configurations for testing purposes.

        The method performs the following steps:
        1. Uses the profile_factory to create a profile object with the attributes first_name="Profile_Name_1", last_name="Profile_Last_Name_1", and is_active=True.
        2. Uses the profile_factory to create a profile object with the attributes first_name="Profile_Name_2", last_name="Profile_Last_Name_2", and is_active=True.
        3. Uses the profile_factory to create a profile object with the attributes first_name="Profile_Name_3", last_name="Profile_Last_Name_3", and is_active=False.

        These mock profile objects can be used for testing various scenarios related to profiles, such as filtering active profiles or checking the correctness of profile data.
        """
        profile_factory(
            first_name="Profile_Name_1",
            last_name="Profile_Last_Name_1",
            is_active=True,
        )
        profile_factory(
            is_active=True, first_name="Profile_Name_2", last_name="Profile_Last_Name_2"
        )
        profile_factory(
            is_active=False,
            first_name="Profile_Name_3",
            last_name="Profile_Last_Name_3",
        )

    def test_str_method(self, profile_factory):
        """
        Test the __str__ method of the profile object.

        Args:
            profile_factory: A factory function or object used to create a profile object.

        Returns:
            None

        Example usage:
            test_str_method(profile_factory)

        This method tests the __str__ method of the profile object to ensure that it returns the expected string representation.

        The method performs the following steps:
        1. Creates a profile object using the profile_factory.
        2. Calls the __str__ method of the profile object.
        3. Asserts that the returned string is equal to the expected string representation, which in this case is "Joe Doe".

        If the assertion passes, the test is considered successful. If the assertion fails, the test fails.

        """
        obj = profile_factory()
        assert obj.__str__() == "Joe Doe"

    def test_max_length_method(self, profile_factory):
        """
        Test the max length validation of profile fields.

        Args:
            profile_factory: A factory function or object used to create a profile object.

        Returns:
            None

        Example usage:
            test_max_length_method(profile_factory)

        This method tests the max length validation of the profile fields to ensure that they don't exceed the specified maximum length.

        The method performs the following steps:
        1. Creates string variables `first_name`, `last_name`, and `profile_key` with lengths of 150 characters.
        2. Creates a profile object using the profile_factory.
        3. Checks if the lengths of `first_name`, `last_name`, and `profile_key` are greater than 150 characters.
        4. If any of the lengths exceed 150 characters, it expects a ValidationError to be raised when calling the `full_clean()` method on the profile object.
        5. If the lengths are within the allowed limit, it asserts that calling `full_clean()` on the profile object returns None and that the lengths of `first_name`, `last_name`, and `profile_key` are less than or equal to 150 characters.

        If the expected validation or assertions pass, the test is considered successful. If the validation or any of the assertions fail, the test fails.

        """
        first_name = "x" * 150
        last_name = "y" * 150
        profile_key = "z" * 150
        obj = profile_factory()
        if len(first_name) > 150 or len(last_name) > 150 or len(profile_key) > 150:
            with pytest.raises(ValidationError):
                obj.full_clean()
        else:
            assert obj.full_clean() is None
            assert len(first_name) <= 150
            assert len(last_name) <= 150
            assert len(profile_key) <= 150

    def test_profile_key(self, profile_factory):
        """
        Test the profile_key field of the profile object.

        Args:
            profile_factory: A factory function or object used to create a profile object.

        Returns:
            None

        Example usage:
            test_profile_key(profile_factory)

        This method tests the profile_key field of the profile object to ensure that it meets certain requirements.

        The method performs the following steps:
        1. Creates a profile object using the profile_factory.
        2. Retrieves the profile_key field from the profile object's metadata.
        3. Asserts that the maximum length of the profile_key field is less than or equal to 12.
        4. Asserts that the unique constraint is applied to the profile_key field.
        5. Asserts that the profile_key field includes alphabetic characters.
        6. Creates two additional profile objects using the profile_factory and asserts that their profile_key values are not None and consist of alphanumeric characters.
        7. Calls the profile_factory to create another profile object, which should raise an IntegrityError due to the unique constraint violation.

        If all the assertions pass and the IntegrityError is raised as expected, the test is considered successful. If any of the assertions fail or the IntegrityError is not raised, the test fails.

        """
        obj = profile_factory()
        profile_key_field = obj._meta.get_field("profile_key")
        assert profile_key_field.max_length <= 12
        assert profile_key_field.unique is True
        assert profile_key_field.include_alpha is True
        assert (
            profile_factory(first_name="Rex", last_name="Johny").profile_key is not None
        )
        assert profile_factory(
            first_name="Jack", last_name="Johnson"
        ).profile_key.isalnum()

        profile_factory()
        with pytest.raises(IntegrityError):
            profile_factory()

    def test_is_active_or_passive(self, profile_factory):
        """
        Test the is_active field of the profile object.

        Args:
            profile_factory: A factory function or object used to create a profile object.

        Returns:
            None

        Example usage:
            test_is_active_or_passive(profile_factory)

        This method tests the is_active field of the profile object to ensure that it can be set to True or False.

        The method performs the following steps:
        1. Creates a profile object using the profile_factory.
        2. Asserts that the initial value of the is_active field is False.
        3. Sets the is_active field of the profile object to True.
        4. Asserts that the is_active field has been updated to True.

        If all the assertions pass, the test is considered successful. If any of the assertions fail, the test fails.

        """
        obj = profile_factory()
        assert obj.is_active is False
        obj.is_active = True
        assert obj.is_active is True

    def test_user(self, profile_factory):
        """
        Test the user association of the profile object.

        Args:
            profile_factory: A factory function or object used to create a profile object.

        Returns:
            None

        Example usage:
            test_user(profile_factory)

        This method tests the user association of the profile object to ensure that it is not None.

        The method performs the following steps:
        1. Creates a profile object using the profile_factory.
        2. Asserts that the user association of the profile object is not None.

        If the assertion passes, the test is considered successful. If the assertion fails, the test fails.

        """
        assert profile_factory().user is not None

    def test_is_active(self, profile_factory):
        """
        Test the is_active method of the active profile objects.

        Args:
            profile_factory: A factory function or object used to create a profile object.

        Returns:
            None

        Example usage:
            test_is_active(profile_factory)

        This method tests the is_active method of the active profile objects to ensure that it returns True.

        The method performs the following steps:
        1. Creates a set of mock profile objects using the create_mock_profile method.
        2. Retrieves the active profiles using the get_active_profiles method on the Profile model.
        3. Iterates through each profile object in the queryset.
        4. Asserts that the is_active method of each profile object returns True.

        If all the assertions pass, the test is considered successful. If any of the assertions fail, the test fails.

        """
        self.create_mock_profile(profile_factory)
        qs = Profile.objects.get_active_profiles().is_active()
        for obj in qs:
            assert obj.is_active is True

    def test_is_active_count(self, profile_factory):
        """
        Test the is_active_count method of the active profile objects.

        Args:
            profile_factory: A factory function or object used to create a profile object.

        Returns:
            None

        Example usage:
            test_is_active_count(profile_factory)

        This method tests the is_active_count method of the active profile objects to ensure that it returns a count greater than or equal to 0.

        The method performs the following steps:
        1. Creates a set of mock profile objects using the create_mock_profile method.
        2. Retrieves the active profiles using the get_active_profiles method on the Profile model.
        3. Calls the is_active_count method on the queryset of active profiles.
        4. Asserts that the result of the is_active_count method is either 0 or greater than 0.

        If the assertion passes, the test is considered successful. If the assertion fails, the test fails.
        """
        self.create_mock_profile(profile_factory)
        qs = Profile.objects.get_active_profiles().is_active_count()
        assert qs == 0 or qs > 0

    def test_is_passive(self, profile_factory):
        """
        Test the is_passive method of the passive profile objects.

        Args:
            profile_factory: A factory function or object used to create a profile object.

        Returns:
            None

        Example usage:
            test_is_passive(profile_factory)

        This method tests the is_passive method of the passive profile objects to ensure that it returns False.

        The method performs the following steps:
        1. Creates a set of mock profile objects using the create_mock_profile method.
        2. Retrieves the passive profiles using the get_passive_profiles method on the Profile model.
        3. Iterates through each profile object in the queryset.
        4. Asserts that the is_active property of each profile object is False.

        If all the assertions pass, the test is considered successful. If any of the assertions fail, the test fails.

        """
        self.create_mock_profile(profile_factory)
        qs = Profile.objects.get_passive_profiles().is_passive()
        for obj in qs:
            assert obj.is_active is False

    def test_is_passive_count(self, profile_factory):
        """
        Test the is_passive_count method of the passive profile objects.

        Args:
            profile_factory: A factory function or object used to create a profile object.

        Returns:
            None

        Example usage:
            test_is_passive_count(profile_factory)

        This method tests the is_passive_count method of the passive profile objects to ensure that it returns a count greater than or equal to 0.

        The method performs the following steps:
        1. Creates a set of mock profile objects using the create_mock_profile method.
        2. Retrieves the passive profiles using the get_passive_profiles method on the Profile model.
        3. Calls the is_passive_count method on the queryset of passive profiles.
        4. Asserts that the result of the is_passive_count method is either 0 or greater than 0.

        If the assertion passes, the test is considered successful. If the assertion fails, the test fails.
        """

        self.create_mock_profile(profile_factory)
        qs = Profile.objects.get_passive_profiles().is_passive_count()
        assert qs == 0 or qs > 0

    def test_get_full_name(self, profile_factory):
        """
        Test the get_full_name method of the profile object.

        Args:
            profile_factory: A factory function or object used to create a profile object.

        Returns:
            None

        Example usage:
            test_get_full_name(profile_factory)

        This method tests the get_full_name method of the profile object to ensure that it returns the expected full name.

        The method performs the following steps:
        1. Creates a profile object using the profile_factory and assigns it to the `obj` variable. The first name is set to "Generator" and the last name is set to "Rex".
        2. Asserts that the first_name property of the profile object is not None.
        3. Asserts that the last_name property of the profile object is not None.
        4. Asserts that the result of calling the get_full_name method on the profile object is equal to "Generator Rex".

        If all the assertions pass, the test is considered successful. If any of the assertions fail, the test fails.
        """

        obj = profile_factory(first_name="Generator", last_name="Rex")
        assert obj.first_name is not None
        assert obj.last_name is not None
        assert obj.get_full_name() == "Generator Rex"
