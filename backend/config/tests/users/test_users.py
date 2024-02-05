import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

# *If you don't declare pytestmark our test class model don't accsess to database table
pytestmark = pytest.mark.django_db


#! TestUsersManagers
class TestUsersManagers:
    def test_create_user(self, user_factory):
        user = user_factory.create()
        assert user.email == "normal_user{}@gmail.com".format(0)
        assert user.is_active
        assert user.is_staff is False
        assert user.is_superuser is False
