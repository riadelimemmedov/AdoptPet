import factories
import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError

from abstract.constants import GendersPet, ImageExtension
from apps.pet.models import Pet
from infrastructure.test_data_clear import TruncateTestData

# *If you don't declare pytestmark our test class model don't accsess to database table
pytestmark = pytest.mark.django_db


# !TestPetManagers
class TestPetManagers:
    def create_mock_pet(self, pet_factory):
        pet_factory(
            name="Max",
            age=3,
            breed="Labrador",
            color="#ff00ff",
            weight=25.5,
            gender="Male",
            pet_photo_url=SimpleUploadedFile("test.jpg", b""),
            location="Street 1",
            city="Chicago",
            status=True,
            vaccinated=True,
            description="Energetic and playful pup",
        )
        pet_factory(
            age=2,
            breed="Golden Retriever",
            color="#f9a602",
            weight=28.7,
            gender="Female",
            pet_photo_url=SimpleUploadedFile("test.jpg", b""),
            location="Park Avenue",
            city="New York",
            status=True,
            vaccinated=True,
            description="Friendly and obedient companion",
        )
        pet_factory(
            name="Charlie",
            age=4,
            breed="Beagle",
            color="#aabbcc",
            weight=15.2,
            gender="Male",
            pet_photo_url=SimpleUploadedFile("test.jpg", b""),
            location="123 Main Street",
            city="Los Angeles",
            status=False,
            vaccinated=True,
            description="Loyal and playful companion",
        )

    def test_str_method(self, pet_factory):
        obj = pet_factory()
        assert obj.__str__() is not None
        TruncateTestData(Pet)

    def test_max_length_method(self, pet_factory):
        name = "a" * 50
        breed = "b" * 50
        gender = "c" * 50
        location = "d" * 50
        city = "e" * 50
        description = "f" * 150
        obj = pet_factory()
        if (
            len(name) > 50
            or len(breed) > 50
            or len(gender) > 50
            or len(location) > 50
            or len(city) > 50
            or len(description) > 150
        ):
            with pytest.raises(ValidationError):
                obj.full_clean()
        else:
            assert len(name) <= 50
            assert len(gender) <= 50
            assert len(location) <= 50
            assert len(city) <= 50
            assert len(description) <= 150
        TruncateTestData(Pet)

    def test_status_active_or_passive(self, pet_factory):
        obj = pet_factory()
        if obj.status:
            assert obj.status is True
        obj.status = False
        assert obj.status is False
        TruncateTestData(Pet)

    def test_pet(self, pet_factory):
        obj = pet_factory()
        assert obj is not None
        TruncateTestData(Pet)

    def test_active_status(self, pet_factory):
        self.create_mock_pet(pet_factory)
        qs = Pet.objects.get_active_status().active_status()
        for obj in qs:
            assert obj.status is True
        TruncateTestData(Pet)

    def test_active_status_count(self, pet_factory):
        self.create_mock_pet(pet_factory)
        qs = Pet.objects.get_active_status().active_status_count()
        assert qs == 0 or qs > 0
        TruncateTestData(Pet)

    def test_passive_status(self, pet_factory):
        self.create_mock_pet(pet_factory)
        qs = Pet.objects.get_passive_status().passive_status()
        for obj in qs:
            assert obj.status is False
        TruncateTestData(Pet)

    def test_passive_status_count(self, pet_factory):
        self.create_mock_pet(pet_factory)
        qs = Pet.objects.get_passive_status().passive_status_count()
        assert qs == 0 or qs > 0
        TruncateTestData(Pet)

    def test_pet_photo_validation(self, pet_factory):
        obj = pet_factory()
        if obj.pet_photo_url not in ImageExtension:
            with pytest.raises(ValidationError):
                obj.full_clean()
        TruncateTestData(Pet)

    def test_age(self, pet_factory):
        obj = pet_factory()
        if obj.age < 0 or obj.age > 15:
            with pytest.raises(ValidationError):
                obj.full_clean()
        TruncateTestData(Pet)

    def test_color(self, pet_factory):
        obj = pet_factory()
        assert obj.color.startswith("#") is True
        TruncateTestData(Pet)

    def test_weight(self, pet_factory):
        obj = pet_factory()
        if obj.weight < 1 or obj.weight > 50:
            with pytest.raises(ValidationError):
                obj.full_clean()
        TruncateTestData(Pet)

    def test_gender(self, pet_factory):
        obj = pet_factory()
        if obj.gender not in GendersPet:
            with pytest.raises(ValidationError):
                obj.full_clean()
        TruncateTestData(Pet)

    def test_pet_creation(self, pet_factory):
        obj = pet_factory(
            name="Max",
            age=3,
            breed="Labrador",
            color="#ff00ff",
            weight=25.5,
            gender="Male",
            pet_photo_url=SimpleUploadedFile("test.jpg", b""),
            location="Street 22",
            city="New York",
            status=True,
            vaccinated=True,
            description="Energetic and playful pup",
        )
        assert obj.created is not None
        assert obj.modified is not None
        TruncateTestData(Pet)
