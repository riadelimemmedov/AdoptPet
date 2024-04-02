import json

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

# * If you don't declare pytestmark our test class model don't accsess to database table
pytestmark = pytest.mark.django_db

# User
User = get_user_model()


# !TestPostCommentEndpoints
class TestPostCommentEndpoints:
    endpoint = "/posts/"

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

    def get_user_object(self, user_id):
        """
        Retrieve a user object by its ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The User object matching the provided user ID.

        Raises:
            User.DoesNotExist: If no user with the provided ID exists.

        """
        user = User.objects.get(id=user_id)
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
    def comment_response(self, api_client, get_user, post_factory):
        """
        Test method to check the response when a user comments on a post.

        Args:
            api_client (function): A function that returns an instance of the API client.
            get_user (tuple): A tuple containing the user information and headers.
            post_factory (function): A function that returns an instance of a post.

        Yields:
            tuple: A tuple containing the payload, response, post, and user.

        """
        user, headers = get_user
        user = self.get_user_object(user.data["id"])
        post = post_factory()
        if user.is_authenticated:
            payload = {
                "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua",
            }
            response = api_client().post(
                f"{self.endpoint}{post.slug}/comment/",
                payload,
                format="json",
                headers=headers,
            )
            yield payload, response, post, user

    def test_create_comment(self, comment_response):
        """
        Test method to verify the creation of a comment.

        Args:
            comment_response (generator): A generator that yields a tuple containing the payload, response, post, and user.

        Returns:
            None

        Raises:
            AssertionError: If the response status code is not HTTP_201_CREATED or if the comment body is None.

        """
        _, response, _, _ = comment_response
        assert response.status_code == status.HTTP_201_CREATED
        assert (response.data["body"]) is not None

    def test_return_all_comments_for_single_post(self, comment_response, api_client):
        """
        Test method to verify the retrieval of all comments for a single post.

        Args:
            comment_response (generator): A generator that yields a tuple containing the payload, response, post, and user.
            api_client (function): A function that returns an instance of the API client.

        Returns:
            None

        Raises:
            AssertionError: If the response status code is not HTTP_200_OK or if the comments' attributes do not match the expected values.

        """
        payload, response, post, user = comment_response
        response = api_client().get(
            f"{self.endpoint}{post.slug}/comment/", format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["author"] == user.username
        assert response.data[0]["created"] is not None
        assert response.data[0]["modified"] is not None
        assert response.data[0]["body"] == payload["body"]
        assert response.data[0]["post"] == post.id

    def test_return_single_comment_for_single_post(self, api_client, comment_response):
        """
        Test method to verify the retrieval of a single comment for a single post.

        Args:
            api_client (function): A function that returns an instance of the API client.
            comment_response (generator): A generator that yields a tuple containing the payload, response, post, and user.

        Returns:
            None

        Raises:
            AssertionError: If the response status code is not HTTP_200_OK or if the comment's attributes do not match the expected values.

        """
        payload, response, post, user = comment_response
        response = api_client().get(
            f"{self.endpoint}{post.slug}/comment/{response.data['id']}/",
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["author"] == user.username
        assert response.data["created"] is not None
        assert response.data["modified"] is not None
        assert response.data["body"] == payload["body"]
        assert response.data["post"] == post.id

    def test_update_single_comment_for_single_post(
        self, api_client, comment_response, get_user
    ):
        """
        Test method to verify the update of a single comment for a single post.

        Args:
            api_client (function): A function that returns an instance of the API client.
            comment_response (generator): A generator that yields a tuple containing the payload, response, post, and user.
            get_user (tuple): A tuple containing the user information and headers.

        Returns:
            None

        Raises:
            AssertionError: If the response status code is not HTTP_200_OK or if the comment body is not updated.

        """
        payload, response, post, _ = comment_response
        _, headers = get_user
        response = api_client().put(
            f"{self.endpoint}{post.slug}/comment/{response.data['id']}/",
            {"body": "Why we need to use python for backend development"},
            headers=headers,
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["body"] != payload["body"]

    def test_delete_single_comment_for_single_post(
        self, api_client, comment_response, get_user
    ):
        """
        Test method to verify the deletion of a single comment for a single post.

        Args:
            api_client (function): A function that returns an instance of the API client.
            comment_response (generator): A generator that yields a tuple containing the payload, response, post, and user.
            get_user (tuple): A tuple containing the user information and headers.

        Returns:
            None

        Raises:
            AssertionError: If the response status code is not HTTP_204_NO_CONTENT.

        """
        _, response, post, _ = comment_response
        _, headers = get_user
        response = api_client().delete(
            f"{self.endpoint}{post.slug}/comment/{response.data['id']}/",
            headers=headers,
            format="json",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
