import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.pet.models import Pet

# *If you don't declare pytestmark our test class model don't accsess to database table
pytestmark = pytest.mark.django_db


# !TestPetManagers
class TestPetManagers:
    def test_str_method(self, pet_factory):
        obj = pet_factory()
        assert obj.__str__() == "Max - 3"
