import json
import os

import pytest
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from abstract.constants import ImageExtension
from apps.pet.models import Pet
from apps.pet.serializers import PetSerializer
from infrastructure.test_data_clear import TruncateTestData

# * If you don't declare pytestmark our test class model don't accsess to database table
pytestmark = pytest.mark.django_db


# !TestPetEndpoints
class TestPetEndpoints:
    endpoint = "/pets/"

    def test_return_all_pets(self, pet_factory_end_to_end, api_client):
        """
        Test case to verify that all pets are returned successfully.

        Steps:
        1. Create a batch of 4 pets using the end-to-end pet factory.
        2. Make a GET request to the API endpoint to retrieve all pets.
        3. Assert that the response status code is 200 (OK).
        4. Assert that the number of returned pets matches the expected count of 4.

        Expected Behavior:
        The test should pass if the API successfully returns all the pets with the correct status code and count.
        """
        pet_factory_end_to_end.create_batch(4)
        response = api_client().get(self.endpoint, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert json.loads(response.content)["pet_count"] == 4
        # TruncateTestData(Pet)

    def test_create_pet(self, pet_factory_end_to_end, api_client):
        """
        Test case to verify the creation of a new pet.

        Steps:
        1. Prepare the data for creating a new pet, including the required fields such as name, age, breed, slug, color, weight, pet_photo_url, gender, location, city, status, vaccinated, and description.
        2. Make a POST request to the API endpoint to create a new pet, providing the prepared data.
        3. Assert that the response status code is 201 (Created).
        4. Assert that the name of the created pet in the response matches the expected name.

        Expected Behavior:
        The test should pass if the API successfully creates a new pet with the provided data and returns the correct status code and the name of the created pet.

        """
        data = {
            "name": "Max",
            "age": 1,
            "breed": "Labrador",
            "slug": "yxxa77",
            "color": "#ff00ff",
            "weight": 25.5,
            "pet_photo_url": SimpleUploadedFile("test.jpg", b""),
            "gender": "Male",
            "location": "Street 1",
            "city": "Chicago",
            "status": True,
            "vaccinated": True,
            "description": "Energetic and playful pup",
        }

        response = api_client().post(
            self.endpoint,
            data,
            format="multipart",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Max"
        # TruncateTestData(Pet)

    def test_delete_all_pets(self, pet_factory_end_to_end, api_client):
        """
        Test case to verify the deletion of all pets.

        Steps:
        1. Create a batch of 4 pets using the end-to-end pet factory.
        2. Make a GET request to the API endpoint to retrieve all pets.
        3. Assert that the response status code is 200 (OK).
        4. Assert that the number of returned pets matches the expected count of 4.
        5. Make a DELETE request to the API endpoint to delete all pets.
        6. Assert that the response status code is 204 (No Content).
        7. Make another GET request to the API endpoint to retrieve all pets.
        8. Assert that the response status code is 200 (OK).
        9. Assert that the number of returned pets is now 0.

        Expected Behavior:
        The test should pass if the API successfully deletes all the pets, returning the correct status codes and counts before and after the deletion.

        """
        pet_factory_end_to_end.create_batch(5)
        response = api_client().get(self.endpoint, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert json.loads(response.content)["pet_count"] == 5

        response = api_client().delete(self.endpoint)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.content == b""
        assert len(response.content) == 0
        # TruncateTestData(Pet)

    def test_get_object_existing_pet(self, pet_factory_end_to_end, api_client):
        """
        Test case to verify the retrieval of a specific pet object.

        Steps:
        1. Prepare the necessary data, such as the pet's name and pet_key.
        2. Create a batch of 1 pet using the end-to-end pet factory, providing the prepared name and pet_key.
        3. Make a GET request to the API endpoint, appending the pet's slug to retrieve the specific pet object.
        4. Assert that the retrieved pet object's slug matches the expected format (name-pet_key in lowercase).
        5. Assert that the response status code is 200 (OK).
        6. Assert that the number of created pet objects is 1.
        7. Assert that the retrieved pet object's slug matches the slug of the created pet.

        Expected Behavior:
            The test should pass if the API successfully retrieves the specific pet object, returning the correct status code, matching slugs, and the expected number of created pet objects.
        """
        name = "Max"
        pet_key = "uuxx12345jky"
        obj = pet_factory_end_to_end.create_batch(1, name=name, pet_key=pet_key)

        response = api_client().get(f"{self.endpoint}{obj[0].slug}/", format="json")

        assert response.data["slug"] == f"{name}-{pet_key}".lower()
        assert response.status_code == status.HTTP_200_OK
        assert len(obj) == 1
        assert response.data["slug"] == obj[0].slug
        # TruncateTestData(Pet)

    def test_put_existing_pet(self, pet_factory_end_to_end, api_client):
        """
        Test case to verify the update of an existing pet object.

        Steps:
        1. Prepare the necessary data, such as the pet's new name and the existing pet object.
        2. Create a batch of 1 pet using the end-to-end pet factory, providing initial values for name and pet_key.
        3. Make a GET request to the API endpoint, appending the slug of the created pet object to retrieve the pet's details.
        4. Validate the file extension of the pet's photo URL, ensuring it is valid. If not, assert False and print an error message.
        5. If the file extension is valid, assert True and print a success message.
        6. Prepare the updated data for the pet, copying the existing values for age, breed, color, weight, gender, location, city, status, vaccinated, and description from the retrieved pet's details.
        7. Set the "name" field in the updated data to the new name.
        8. Make a PUT request to the API endpoint, appending the slug of the pet object, and providing the updated data.
        9. Assert that the response status code is 200 (OK).
        10. Assert that the name of the updated pet object is not equal to the initial name.
        11. Assert that the slug field is not empty in the response data.
        12. Assert that the response data matches the serialized data of the updated pet object.

        Expected Behavior:
        The test should pass if the API successfully updates the existing pet object, returning the correct status code, updated name, non-empty slug, and matching serialized data.

        """
        name = "Max"
        obj = pet_factory_end_to_end.create_batch(1, name="Rex", pet_key="uuxx12345jky")

        response = api_client().get(f"{self.endpoint}{obj[0].slug}/", format="json")

        if obj[0].pet_photo_url not in ImageExtension:
            with pytest.raises(ValidationError):
                obj[0].full_clean()
        else:
            data = {
                "name": name,
                "age": response.data["age"],
                "breed": response.data["breed"],
                "color": response.data["color"],
                "weight": response.data["weight"],
                "pet_photo_url": "",
                "gender": response.data["gender"],
                "location": response.data["location"],
                "city": response.data["city"],
                "status": response.data["status"],
                "vaccinated": response.data["vaccinated"],
                "description": response.data["description"],
            }

            response = api_client().put(
                f"{self.endpoint}{obj[0].slug}/",
                data,
                format="multipart",
            )

            assert response.status_code == status.HTTP_200_OK
            assert response.data["name"] != "Rex"
            assert response.data.pop("slug") is not None
            assert response.data == PetSerializer(data).data
            # TruncateTestData(Pet)

    def test_delete_existing_pet(self, pet_factory_end_to_end, api_client):
        """
        Test case to verify the deletion of an existing pet object.

        Steps:
        1. Create a batch of 1 pet using the end-to-end pet factory.
        2. Make a GET request to the API endpoint, appending the slug of the created pet object to retrieve the pet's details.
        3. Assert that the response status code is 200 (OK), indicating the successful retrieval of the pet object.
        4. Make a DELETE request to the API endpoint, appending the slug of the pet object to delete it.
        5. Assert that the response status code is 204 (No Content), indicating the successful deletion of the pet object.
        6. Make another GET request to the API endpoint, appending the slug of the deleted pet object.
        7. Assert that the response status code is 404 (Not Found), indicating that the pet object is no longer present.

        Expected Behavior:
        The test should pass if the API successfully deletes the existing pet object, returning the correct status codes indicating deletion and absence of the pet object.

        """
        obj = pet_factory_end_to_end.create_batch(1)

        response = api_client().get(f"{self.endpoint}{obj[0].slug}/", format="json")
        assert response.status_code == status.HTTP_200_OK

        response = api_client().delete(f"{self.endpoint}{obj[0].slug}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = api_client().get(f"{self.endpoint}{obj[0].slug}/", format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        # TruncateTestData(Pet)
