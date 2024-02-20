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
        """
        Creates mock pet objects using the provided pet_factory.

        Args:
            pet_factory: A factory function or object used to create pet objects.

        Returns:
            None

        Example usage:
            create_mock_pet(pet_factory)
        """

        pet_factory(
            name="Max",
            age=3,
            breed="Labrador",
            slug="yxxa77",
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
            slug="yxghjk88pa",
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
            slug="ghjkjdha5577uj",
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
        """
        Test the __str__ method of the pet object created by the pet_factory.

        Args:
            pet_factory: A factory function or object used to create a pet object.

        Returns:
            None

        This method tests the __str__ method of the pet object created by the pet_factory. It ensures that the __str__ method returns a non-empty value.

        The method performs the following steps:
        1. Creates a pet object using the pet_factory.
        2. Asserts that the __str__ method of the object is not None.

        If the assertion passes, the test is considered successful. If the assertion fails, an AssertionError is raised.

        After testing the __str__ method, the test method calls the TruncateTestData function to truncate the test data for the Pet model. This ensures a clean state for subsequent tests.

        """
        obj = pet_factory()
        assert obj.__str__() is not None
        TruncateTestData(Pet)

    def test_slug(self, pet_factory):
        """
        Test the slug attribute of the pet object created by the pet_factory.

        Args:
            pet_factory: A factory function or object used to create a pet object.

        Returns:
            None

        Example usage:
            test_slug(pet_factory)

        This method tests the slug attribute of the pet object created by the pet_factory. It verifies that the slug is generated correctly based on the name and pet_key attributes.

        The method performs the following steps:
        1. Creates a pet object using the pet_factory, with a specific name and pet_key.
        2. Saves the pet object to persist it in the database.
        3. Asserts that the slug attribute of the object is equal to the concatenation of the name and pet_key (converted to lowercase) separated by a hyphen.

        If the assertion passes, the test is considered successful. If the assertion fails, an AssertionError is raised.

        After testing the slug attribute, the test method calls the TruncateTestData function to truncate the test data for the Pet model. This ensures a clean state for subsequent tests.

        """

        obj = pet_factory(name="rex", pet_key="iamptoswoqgy")
        obj.save()
        assert obj.slug == f"{obj.name}-{obj.pet_key.lower()}"
        TruncateTestData(Pet)

    def test_max_length_method(self, pet_factory):
        """
        Test the maximum length constraints of the fields in the pet object.

        Args:
            pet_factory: A factory function or object used to create a pet object.

        Returns:
            None

        Example usage:
            test_max_length_method(pet_factory)

        This method tests the maximum length constraints of the fields in the pet object created by the pet_factory. It ensures that the length of each field does not exceed the specified maximum length.

        The method performs the following steps:
        1. Sets up variables with values that exceed the maximum length for the respective fields (name, breed, gender, location, city, and description).
        2. Creates a pet object using the pet_factory.
        3. If any of the field values exceed the maximum length, the method asserts that an instance of ValidationError is raised when calling the `full_clean()` method of the pet object.
        4. If all field values are within the maximum length constraints, the method asserts that the length of each field is less than or equal to the respective maximum length.

        If the assertions pass, the test is considered successful. If any of the assertions fail or if a ValidationError is not raised when expected, an AssertionError is raised.

        After testing the maximum length constraints, the test method calls the TruncateTestData function to truncate the test data for the Pet model. This ensures a clean state for subsequent tests.

        """

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
        """
        Test the status attribute of the pet object to ensure it represents active or passive status correctly.

        Args:
            pet_factory: A factory function or object used to create a pet object.

        Returns:
            None

        Example usage:
            test_status_active_or_passive(pet_factory)

        This method tests the status attribute of the pet object created by the pet_factory. It verifies that the status is correctly represented as either active or passive.

        The method performs the following steps:
        1. Creates a pet object using the pet_factory.
        2. If the initial value of the status attribute is truthy (evaluates to True), the method asserts that the status is True.
        3. Updates the status attribute to False.
        4. Asserts that the updated value of the status attribute is False.

        If the assertions pass, the test is considered successful. If any of the assertions fail, an AssertionError is raised.

        After testing the status attribute, the test method calls the TruncateTestData function to truncate the test data for the Pet model. This ensures a clean state for subsequent tests.

        """
        obj = pet_factory()
        if obj.status:
            assert obj.status is True
        obj.status = False
        assert obj.status is False
        TruncateTestData(Pet)

    def test_pet(self, pet_factory):
        """
        Test the creation of a pet object using the pet_factory.

        Args:
            pet_factory: A factory function or object used to create a pet object.

        Returns:
            None

        Example usage:
            test_pet(pet_factory)

        This method tests the creation of a pet object using the pet_factory. It verifies that the object is successfully created and is not None.

        The method performs the following steps:
        1. Creates a pet object using the pet_factory.
        2. Asserts that the created object is not None.

        If the assertion passes, the test is considered successful. If the assertion fails and the object is None, an AssertionError is raised.

        After testing the creation of the pet object, the test method calls the TruncateTestData function to truncate the test data for the Pet model. This ensures a clean state for subsequent tests.

        """

        obj = pet_factory()
        assert obj is not None
        TruncateTestData(Pet)

    def test_active_status(self, pet_factory):
        """
        Test the retrieval of pet objects with an active status.

        Args:
            pet_factory: A factory function or object used to create a pet object.

        Returns:
            None

        Example usage:
            test_active_status(pet_factory)

        This method tests the retrieval of pet objects with an active status using the `get_active_status()` and `active_status()` methods of the Pet model's queryset.

        The method performs the following steps:
        1. Creates a mock pet object using the pet_factory.
        2. Retrieves the queryset of pet objects with an active status by chaining the `get_active_status()` and `active_status()` methods.
        3. Iterates over each pet object in the queryset and asserts that the status attribute is True.

        If all the assertions pass for each pet object in the queryset, the test is considered successful. If any of the assertions fail, an AssertionError is raised.

        After testing the retrieval of pet objects with an active status, the test method calls the TruncateTestData function to truncate the test data for the Pet model. This ensures a clean state for subsequent tests.

        """
        self.create_mock_pet(pet_factory)
        qs = Pet.objects.get_active_status().active_status()
        for obj in qs:
            assert obj.status is True
        TruncateTestData(Pet)

    def test_active_status_count(self, pet_factory):
        """
        Test the count of pet objects with an active status.

        Args:
            pet_factory: A factory function or object used to create a pet object.

        Returns:
            None

        Example usage:
            test_active_status_count(pet_factory)

        This method tests the count of pet objects with an active status using the `get_active_status()` and `active_status_count()` methods of the Pet model's queryset.

        The method performs the following steps:
        1. Creates a mock pet object using the pet_factory.
        2. Retrieves the count of pet objects with an active status using the `get_active_status()` and `active_status_count()` methods.
        3. Asserts that the count value is either 0 or greater than 0.

        If the assertion passes, the test is considered successful. If the assertion fails and the count value is less than 0, an AssertionError is raised.

        After testing the count of pet objects with an active status, the test method calls the TruncateTestData function to truncate the test data for the Pet model. This ensures a clean state for subsequent tests.

        """
        self.create_mock_pet(pet_factory)
        qs = Pet.objects.get_active_status().active_status_count()
        assert qs == 0 or qs > 0
        TruncateTestData(Pet)

    def test_passive_status(self, pet_factory):
        """
        Test the retrieval of pet objects with a passive status.

        Args:
            pet_factory: A factory function or object used to create a pet object.

        Returns:
            None

        Example usage:
            test_passive_status(pet_factory)

        This method tests the retrieval of pet objects with a passive status using the `get_passive_status()` and `passive_status()` methods of the Pet model's queryset.

        The method performs the following steps:
        1. Creates a mock pet object using the pet_factory.
        2. Retrieves the queryset of pet objects with a passive status by chaining the `get_passive_status()` and `passive_status()` methods.
        3. Iterates over each pet object in the queryset and asserts that the status attribute is False.

        If all the assertions pass for each pet object in the queryset, the test is considered successful. If any of the assertions fail, an AssertionError is raised.

        After testing the retrieval of pet objects with a passive status, the test method calls the TruncateTestData function to truncate the test data for the Pet model. This ensures a clean state for subsequent tests.

        """
        self.create_mock_pet(pet_factory)
        qs = Pet.objects.get_passive_status().passive_status()
        for obj in qs:
            assert obj.status is False
        TruncateTestData(Pet)

    def test_passive_status_count(self, pet_factory):
        """
        Test the count of pet objects with a passive status.

        Args:
            pet_factory: A factory function or object used to create a pet object.

        Returns:
            None

        Example usage:
            test_passive_status_count(pet_factory)

        This method tests the count of pet objects with a passive status using the `get_passive_status()` and `passive_status_count()` methods of the Pet model's queryset.

        The method performs the following steps:
        1. Creates a mock pet object using the pet_factory.
        2. Retrieves the count of pet objects with a passive status using the `get_passive_status()` and `passive_status_count()` methods.
        3. Asserts that the count value is either 0 or greater than 0.

        If the assertion passes, the test is considered successful. If the assertion fails and the count value is less than 0, an AssertionError is raised.

        After testing the count of pet objects with a passive status, the test method calls the TruncateTestData function to truncate the test data for the Pet model. This ensures a clean state for subsequent tests.

        """
        self.create_mock_pet(pet_factory)
        qs = Pet.objects.get_passive_status().passive_status_count()
        assert qs == 0 or qs > 0
        TruncateTestData(Pet)

    def test_pet_photo_validation(self, pet_factory):
        """
        Test the validation of the pet photo URL.

        Args:
            pet_factory: A factory function or object used to create a pet object.

        Returns:
            None

        Example usage:
            test_pet_photo_validation(pet_factory)

        This method tests the validation of the pet photo URL by checking if it has a valid image extension.

        The method performs the following steps:
        1. Creates a pet object using the pet_factory.
        2. Checks if the pet photo URL has a valid image extension by comparing it against the ImageExtension list or set.
        3. If the pet photo URL does not have a valid image extension, it expects a ValidationError to be raised when calling the `full_clean()` method on the pet object.

        If the expected ValidationError is raised, the test is considered successful. If the pet photo URL has a valid image extension or no ValidationError is raised, the test fails.

        After testing the pet photo URL validation, the test method calls the TruncateTestData function to truncate the test data for the Pet model. This ensures a clean state for subsequent tests.

        """
        obj = pet_factory()
        if obj.pet_photo_url not in ImageExtension:
            with pytest.raises(ValidationError):
                obj.full_clean()
        TruncateTestData(Pet)

    def test_age(self, pet_factory):
        """
        Test the validation of the pet's age.

        Args:
            pet_factory: A factory function or object used to create a pet object.

        Returns:
            None

        Example usage:
            test_age(pet_factory)

        This method tests the validation of the pet's age by checking if it falls within a valid range.

        The method performs the following steps:
        1. Creates a pet object using the pet_factory.
        2. Checks if the pet's age is less than 0 or greater than 15.
        3. If the pet's age is outside the valid range, it expects a ValidationError to be raised when calling the `full_clean()` method on the pet object.

        If the expected ValidationError is raised, the test is considered successful. If the pet's age falls within the valid range or no ValidationError is raised, the test fails.

        After testing the pet's age validation, the test method calls the TruncateTestData function to truncate the test data for the Pet model. This ensures a clean state for subsequent tests.

        """
        obj = pet_factory()
        if obj.age < 0 or obj.age > 15:
            with pytest.raises(ValidationError):
                obj.full_clean()
        TruncateTestData(Pet)

    def test_color(self, pet_factory):
        """
        Test the format of the pet's color.

        Args:
            pet_factory: A factory function or object used to create a pet object.

        Returns:
            None

        Example usage:
            test_color(pet_factory)

        This method tests the format of the pet's color by checking if it starts with a '#' character.

        The method performs the following steps:
        1. Creates a pet object using the pet_factory.
        2. Asserts that the pet's color starts with a '#' character.

        If the assertion passes, the test is considered successful. If the assertion fails, the test fails.

        After testing the pet's color format, the test method calls the TruncateTestData function to truncate the test data for the Pet model. This ensures a clean state for subsequent tests.

        """
        obj = pet_factory()
        assert obj.color.startswith("#") is True
        TruncateTestData(Pet)

    def test_weight(self, pet_factory):
        """
        Test the validation of the pet's weight.

        Args:
            pet_factory: A factory function or object used to create a pet object.

        Returns:
            None

        Example usage:
            test_weight(pet_factory)

        This method tests the validation of the pet's weight by checking if it falls within a valid range.

        The method performs the following steps:
        1. Creates a pet object using the pet_factory.
        2. Checks if the pet's weight is less than 1 or greater than 50.
        3. If the pet's weight is outside the valid range, it expects a ValidationError to be raised when calling the `full_clean()` method on the pet object.

        If the expected ValidationError is raised, the test is considered successful. If the pet's weight falls within the valid range or no ValidationError is raised, the test fails.

        After testing the pet's weight validation, the test method calls the TruncateTestData function to truncate the test data for the Pet model. This ensures a clean state for subsequent tests.

        """
        obj = pet_factory()
        if obj.weight < 1 or obj.weight > 50:
            with pytest.raises(ValidationError):
                obj.full_clean()
        TruncateTestData(Pet)

    def test_gender(self, pet_factory):
        """
        Test the validation of the pet's gender.

        Args:
            pet_factory: A factory function or object used to create a pet object.

        Returns:
            None

        Example usage:
            test_gender(pet_factory)

        This method tests the validation of the pet's gender by checking if it is one of the valid gender values.

        The method performs the following steps:
        1. Creates a pet object using the pet_factory.
        2. Checks if the pet's gender is not in the GendersPet list or set.
        3. If the pet's gender is not one of the valid values, it expects a ValidationError to be raised when calling the `full_clean()` method on the pet object.

        If the expected ValidationError is raised, the test is considered successful. If the pet's gender is a valid value or no ValidationError is raised, the test fails.

        After testing the pet's gender validation, the test method calls the TruncateTestData function to truncate the test data for the Pet model. This ensures a clean state for subsequent tests.

        """
        obj = pet_factory()
        if obj.gender not in GendersPet:
            with pytest.raises(ValidationError):
                obj.full_clean()
        TruncateTestData(Pet)

    def test_pet_creation(self, pet_factory):
        """
        Test the creation of a pet object.

        Args:
            pet_factory: A factory function or object used to create a pet object.

        Returns:
            None

        Example usage:
            test_pet_creation(pet_factory)

        This method tests the creation of a pet object by providing the necessary attributes.

        The method performs the following steps:
        1. Creates a pet object using the pet_factory and provides the required attributes such as name, age, breed, color, weight, gender, pet_photo_url, location, city, status, vaccinated, and description.
        2. Asserts that the `created` attribute of the pet object is not None, indicating that the pet object was successfully created.
        3. Asserts that the `modified` attribute of the pet object is not None, indicating that the pet object was successfully modified.

        If both assertions pass, the test is considered successful. If any of the assertions fail, the test fails.

        After testing the pet creation, the test method calls the TruncateTestData function to truncate the test data for the Pet model. This ensures a clean state for subsequent tests.
        """
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
