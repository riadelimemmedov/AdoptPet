import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

# *If you don't declare pytestmark our test class model don't accsess to database table
pytestmark = pytest.mark.django_db


class TestUserProfileManagers:
    def test_str_method(self, profile_factory):
        obj = profile_factory()
        assert obj.__str__() == "Joe Doe"
