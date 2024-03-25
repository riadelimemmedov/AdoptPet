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


# !TestUserAuthenticationEndpoints
class TestUserAuthenticationEndpoints:
    endpoint = "/users"

    def get_register_payload(self):
        """
        Get the payload for user registration.

        This method returns a dictionary containing the payload data for user registration. The payload includes the following fields:
        - 'username': The username of the user.
        - 'email': The email address of the user.
        - 'password': The password for the user account.
        - 'wallet_address': The wallet address associated with the user.

        Returns:
            dict: A dictionary containing the payload data for user registration.

        Example:
            {
                'username': 'User',
                'email': 'user@mail.ru',
                'password': 'complexpassword123',
                'wallet_address': '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
            }
        """
        return {
            "username": "User",
            "email": "user@mail.ru",
            "password": "complexpassword123",
            "wallet_address": "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266",
        }

    def test_register(self, api_client):
        """
        Test the registration endpoint.

        This method tests the registration functionality by sending a POST request to the registration endpoint
        with the provided payload. It asserts that the response status code is HTTP 201 Created and checks
        that the returned data contains the expected values.

        Args:
            api_client: An instance of the API client.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        payload = self.get_register_payload()

        response = api_client().post(
            f"{self.endpoint}/register/", payload, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] is not None
        assert response.data["username"] == payload["username"]
        assert response.data["email"] == payload["email"]
        assert response.data["wallet_address"] == payload["wallet_address"]
        assert (
            response.data["tokens"]["refresh"] and response.data["tokens"]["access"]
        ) is not None

    def test_login(self, api_client):
        """
        Test the login endpoint.

        This method tests the login functionality by performing the following steps:
        1. Registers a user by sending a POST request to the registration endpoint with the provided payload.
        2. Sends a POST request to the login endpoint with the email and password from the registration payload.
        3. Asserts that the response status code is HTTP 200 OK and checks that the returned data contains the expected values.

        Args:
            api_client: An instance of the API client.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        payload = self.get_register_payload()
        response_register = api_client().post(
            f"{self.endpoint}/register/", payload, format="json"
        )

        login_payload = {
            "email": payload["email"],
            "password": payload["password"],
        }

        response_login = api_client().post(
            f"{self.endpoint}/login/", login_payload, format="json"
        )
        assert response_login.status_code == status.HTTP_200_OK
        assert response_login.data["id"] is not None
        assert response_login.data["username"] == response_register.data["username"]
        assert response_login.data["email"] == response_register.data["email"]
        assert (
            response_login.data["wallet_address"]
            == response_register.data["wallet_address"]
        )
        assert (
            response_login.data["tokens"]["refresh"]
            and response_login.data["tokens"]["access"]
        ) is not None

    def test_logout(self, api_client):
        """
        Test the logout endpoint.

        This method tests the logout functionality by performing the following steps:
        1. Registers a user by sending a POST request to the registration endpoint with the provided payload.
        2. Extracts the refresh token and access token from the registration response.
        3. Sets the authorization header using the access token.
        4. Sends a POST request to the logout endpoint with the refresh token in the payload and the authorization header.
        5. Asserts that the response status code is HTTP 205 Reset Content.

        Args:
            api_client: An instance of the API client.

        Returns:
            None

        Raises:
            AssertionError: If the assertion fails.
        """
        payload = self.get_register_payload()
        response_register = api_client().post(
            f"{self.endpoint}/register/", payload, format="json"
        )
        refresh_token = response_register.data["tokens"]["refresh"]
        access_token = response_register.data["tokens"]["access"]
        headers = {"Authorization": f"Bearer {access_token}"}

        logout_payload = {"refresh": refresh_token}
        response_logout = api_client().post(
            f"{self.endpoint}/logout/", logout_payload, headers=headers, format="json"
        )
        assert response_logout.status_code == status.HTTP_205_RESET_CONTENT

    def test_token_refresh(self, api_client):
        """
        Test the token refresh endpoint.

        This method tests the token refresh functionality by performing the following steps:
        1. Registers a user by sending a POST request to the registration endpoint with the provided payload.
        2. Performs two token refresh requests using the refresh token from the registration response.
            - In the first request, it asserts that the response status code is HTTP 200 OK and checks that the returned data
                contains the new access and refresh tokens.
            - In the second request, it asserts that the response status code is HTTP 401 UNAUTHORIZED and checks that the
                returned data contains the expected error detail and code.

        Args:
            api_client: An instance of the API client.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        payload = self.get_register_payload()
        response_register = api_client().post(
            f"{self.endpoint}/register/", payload, format="json"
        )
        for req_index in range(1, 3):
            refresh_payload = {"refresh": response_register.data["tokens"]["refresh"]}
            response_refresh = api_client().post(
                f"{self.endpoint}/token/refresh/", refresh_payload, format="json"
            )
            if req_index == 1:
                assert response_refresh.status_code == status.HTTP_200_OK
                assert (
                    response_refresh.data["access"] and response_refresh.data["refresh"]
                ) is not None
            elif req_index == 2:
                assert response_refresh.status_code == status.HTTP_401_UNAUTHORIZED
                assert (response_refresh.data["detail"]) == "Token is blacklisted"
                assert (response_refresh.data["code"]) == "token_not_valid"
            else:
                assert True

    def test_get_user(self, api_client):
        """
        Test the get user endpoint.

        This method tests the get user functionality by performing the following steps:
        1. Registers a user by sending a POST request to the registration endpoint with the provided payload.
        2. Extracts the access token from the registration response.
        3. Sets the authorization header using the access token.
        4. Sends a GET request to the get user endpoint with the authorization header.
        5. Asserts that the response status code is HTTP 200 OK and checks that the returned data contains the expected values.

        Args:
            api_client: An instance of the API client.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        payload = self.get_register_payload()
        response_register = api_client().post(
            f"{self.endpoint}/register/", payload, format="json"
        )
        access_token = response_register.data["tokens"]["access"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response_user = api_client().get(f"{self.endpoint}/", headers=headers)
        assert response_user.status_code == status.HTTP_200_OK
        assert response_user.data["id"] is not None
        assert response_user.data["username"] == payload["username"]
        assert response_user.data["email"] == payload["email"]
        assert response_user.data["wallet_address"] == payload["wallet_address"]
