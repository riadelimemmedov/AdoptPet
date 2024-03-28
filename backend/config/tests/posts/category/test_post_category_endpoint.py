import json

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

# * If you don't declare pytestmark our test class model don't accsess to database table
pytestmark = pytest.mark.django_db

# User
User = get_user_model()


# !TestPostsCategoryEndpoints
class TestPostsCategoryEndpoints:
    endpoint = "/posts/categories/"

    def get_register_payload(self):
        """
        Returns a dictionary representing the payload for user registration.

        Returns:
        dict: The payload containing user information.
        """
        return {
            "username": "User",
            "email": "user@mail.ru",
            "password": "complexpassword123",
            "wallet_address": "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266",
        }

    def get_staff_user(self, user_id):
        """
        Retrieves a user by their ID and sets them as a staff user.

        Parameters:
        user_id (int): The ID of the user.

        Returns:
        User: The modified user object.
        """
        user = User.objects.get(id=user_id)
        user.is_staff = True
        user.save()
        return user

    @pytest.fixture
    def register_response(self, api_client):
        """
        Performs a user registration request using the provided API client.

        Parameters:
        api_client (function): A callable representing the API client.

        Yields:
        tuple: A tuple containing the payload and the registration response.
        """
        payload = self.get_register_payload()
        response = api_client().post("/users/register/", payload, format="json")
        yield payload, response

    @pytest.fixture
    def get_user(self, register_response, api_client):
        """
        Retrieves user information using the provided registration response and API client.

        Parameters:
        register_response (tuple): A tuple containing the payload and registration response.
        api_client (function): A callable representing the API client.

        Yields:
        tuple: A tuple containing the user and request headers.
        """
        payload, response = register_response
        access_token = response.data["tokens"]["access"]
        headers = {"Authorization": f"Bearer {access_token}"}
        user = api_client().get("/users/", headers=headers)
        yield user, headers

    @pytest.fixture
    def category_response(self, api_client, get_user):
        """
        Performs a category creation request using the provided API client and user information.

        Parameters:
        api_client (function): A callable representing the API client.
        get_user (tuple): A tuple containing the user information and request headers.

        Yields:
        tuple: A tuple containing the payload and the category creation response.
        """
        user, headers = get_user
        user = self.get_staff_user(user.data["id"])
        if user.is_staff and user.is_authenticated:
            payload = {"name": "devops", "slug": "devops"}
            response = api_client().post(
                f"{self.endpoint}", payload, format="json", headers=headers
            )
            yield payload, response

    def test_return_all_categories(self, category_factory, api_client):
        """
        Test case for returning all categories.

        Parameters:
        category_factory: A factory object for creating categories.
        api_client (function): A callable representing the API client.
        """
        category_factory.create_batch(4)
        response = api_client().get(self.endpoint, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert len(json.loads(response.content)) == 4

    def test_create_category(self, category_response, api_client):
        """
        Test case for creating a category.

        Parameters:
        category_response (tuple): A tuple containing the payload and category creation response.
        api_client (function): A callable representing the API client.
        """
        payload, response = category_response
        assert response.status_code == status.HTTP_201_CREATED
        assert json.loads(response.content) == payload

    def test_get_category(self, category_response, api_client):
        """
        Test case for retrieving a category.

        Parameters:
        category_response (tuple): A tuple containing the payload and category creation response.
        api_client (function): A callable representing the API client.
        """
        payload, response = category_response
        category = api_client().get(
            f"{self.endpoint}{response.data['slug']}/", format="json"
        )
        assert category.status_code == status.HTTP_200_OK

    def test_update_category(self, category_response, get_user, api_client):
        """
        Test case for updating a category.

        Parameters:
        category_response (tuple): A tuple containing the payload and category creation response.
        get_user (tuple): A tuple containing the user information and request headers.
        api_client (function): A callable representing the API client.
        """
        payload, response = category_response
        user, headers = get_user
        updated_category_obj = {"name": "backend"}
        updated_category = api_client().put(  # patch and put same thing for this process because we have only update one field for each request
            f"{self.endpoint}{response.data['slug']}/",
            updated_category_obj,
            headers=headers,
            format="json",
        )
        assert updated_category.status_code == status.HTTP_200_OK
        assert json.loads(updated_category.content) != updated_category_obj
        assert (
            json.loads(updated_category.content)["name"] == updated_category_obj["name"]
        )
        assert (
            json.loads(updated_category.content)["slug"] == updated_category_obj["name"]
        )
        assert json.loads(updated_category.content)["slug"] != response.data["slug"]

    def test_delete_category(self, category_response, get_user, api_client):
        """
        Test case for deleting a category.

        Parameters:
        category_response (tuple): A tuple containing the payload and category creation response.
        get_user (tuple): A tuple containing the user information and request headers.
        api_client (function): A callable representing the API client.
        """
        payload, response = category_response
        user, headers = get_user
        category = api_client().delete(
            f"{self.endpoint}{response.data['slug']}/", headers=headers, format="json"
        )
        assert category.status_code == status.HTTP_204_NO_CONTENT
