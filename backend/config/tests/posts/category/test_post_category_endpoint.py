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
        return {
            "username": "User",
            "email": "user@mail.ru",
            "password": "complexpassword123",
            "wallet_address": "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266",
        }

    @pytest.fixture
    def category_response(self, api_client):
        payload = {"name": "devops"}
        response = api_client().post(f"{self.endpoint}", payload, format="json")
        yield payload, response

    @pytest.fixture
    def register_response(self, api_client):
        payload = self.get_register_payload()
        response = api_client().post("/users/register/", payload, format="json")
        yield payload, response

    @pytest.fixture
    def get_user(self, register_response, api_client):
        payload, response = register_response
        access_token = response.data["tokens"]["access"]
        headers = {"Authorization": f"Bearer {access_token}"}
        user = api_client().get("/users/", headers=headers)
        yield user, headers

    def test_return_all_categories(self, category_factory, api_client):
        category_factory.create_batch(4)
        response = api_client().get(self.endpoint, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert len(json.loads(response.content)) == 4

    def test_create_category(self, get_user, api_client):
        user, headers = get_user
        user = User.objects.get(id=user.data["id"])
        user.is_staff = True
        user.save()
        if user.is_superuser and user.is_authenticated:
            payload = {"name": "devops"}
            response = api_client().post(
                f"{self.endpoint}", payload, format="json", headers=headers
            )
            assert response.status_code == status.HTTP_201_CREATED
            assert json.loads(response.content) == payload
