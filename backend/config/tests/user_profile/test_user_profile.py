import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.user_profile.models import Profile

# *If you don't declare pytestmark our test class model don't accsess to database table
pytestmark = pytest.mark.django_db


# !TestUserProfileManagers
class TestUserProfileManagers:
    def create_mock_profile(self, profile_factory):
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
        obj = profile_factory()
        assert obj.__str__() == "Joe Doe"

    def test_max_length_method(self, profile_factory):
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
        obj = profile_factory()
        assert obj.is_active is False
        obj.is_active = True
        assert obj.is_active is True

    def test_user(self, profile_factory):
        assert profile_factory().user is not None

    def test_is_active(self, profile_factory):
        self.create_mock_profile(profile_factory)
        qs = Profile.objects.get_active_profiles().is_active()
        for obj in qs:
            assert obj.is_active is True

    def test_is_active_count(self, profile_factory):
        self.create_mock_profile(profile_factory)
        qs = Profile.objects.get_active_profiles().is_active_count()
        assert qs == 0 or qs > 0

    def test_is_passive(self, profile_factory):
        self.create_mock_profile(profile_factory)
        qs = Profile.objects.get_passive_profiles().is_passive()
        for obj in qs:
            assert obj.is_active is False

    def test_is_passive_count(self, profile_factory):
        self.create_mock_profile(profile_factory)
        qs = Profile.objects.get_passive_profiles().is_passive_count()
        assert qs == 0 or qs > 0

    def test_get_full_name(self, profile_factory):
        obj = profile_factory(first_name="Generator", last_name="Rex")
        assert obj.first_name is not None
        assert obj.last_name is not None
        assert obj.get_full_name() == "Generator Rex"
