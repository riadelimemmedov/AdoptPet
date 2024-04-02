import json

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

# * If you don't declare pytestmark our test class model don't accsess to database table
pytestmark = pytest.mark.django_db

# User
User = get_user_model()


# !TestPostsEndpoints
class TestPostsEndpoints:
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
    def post_response(self, api_client, get_user, post_factory, category_factory):
        """
        Perform a POST request to create a new post.

        Args:
            api_client (APIClient): The API client used to make the request.
            get_user (tuple): A tuple containing the user data and headers.
            post_factory (factory.Factory): The factory used to create post instances.
            category_factory (factory.Factory): The factory used to create category instances.

        Yields:
            tuple: A tuple containing the payload, response, and user.

        """
        user, headers = get_user
        user = self.get_user_object(user.data["id"])
        if user.is_authenticated:
            payload = {
                "post_photo_url": SimpleUploadedFile("test.jpg", b"xxxxxxxx"),
                "title": "Python",
                "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua",
                "categories": [category_factory().id],
            }
            response = api_client().post(
                self.endpoint, payload, format="multipart", headers=headers
            )
            yield payload, response

    def test_return_all_posts(self, post_factory, api_client):
        """
        Test the endpoint to return all posts.

        Args:
            post_factory (factory.Factory): The factory used to create post instances.
            api_client (APIClient): The API client used to make the request.

        """
        post_factory.create_batch(4)
        response = api_client().get(self.endpoint, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert len(json.loads(response.content)) == 4

    def test_return_single_post(self, post_response, get_user, api_client):
        """
        Test the endpoint to return a single post.

        Args:
            post_response (tuple): A tuple containing the payload, response, and user.
            api_client (APIClient): The API client used to make the request.

        """
        payload, response = post_response
        user, headers = get_user
        user = self.get_user_object(user.data["id"])
        response = api_client().get(
            f"{self.endpoint}{response.data['slug']}/", format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["author"] == user.username

    def test_create_post(self, post_response, api_client):
        """
        Test the endpoint to create a post.

        Args:
            post_response (tuple): A tuple containing the payload, response, and user.
            api_client (APIClient): The API client used to make the request.

        """
        payload, response = post_response
        assert response.status_code == status.HTTP_201_CREATED
        assert (
            response.data["id"]
            and response.data["post_photo_url"]
            and response.data["title"]
            and response.data["body"]
            and response.data["categories"]
            and response.data["slug"]
            and response.data["created"]
            and response.data["modified"]
        ) is not None

    def test_update_post_fields(self, post_response, get_user, api_client):
        """
        Test updating post fields via the API.

        Args:
            post_response: A fixture that provides the initial post data and response.
            get_user: A fixture that provides the authenticated user and headers.
            api_client: A fixture that provides the API client.

        Returns:
            None

        Raises:
            AssertionError: If any of the assertions fail.
        """
        payload, response = post_response
        user, headers = get_user
        title = "Kotlin"
        body = "Why we need to use kotlin"
        post_photo_url = SimpleUploadedFile("test.jpg", b"xxxxxxxx")
        payload["title"] = title
        payload["body"] = body
        payload["post_photo_url"] = post_photo_url
        response = api_client().put(
            f"{self.endpoint}{response.data['slug']}/",
            payload,
            format="multipart",
            headers=headers,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == title
        assert response.data["body"] == body
        assert response.data["post_photo_url"] != post_photo_url.name

    def test_update_post_field(self, post_response, get_user, api_client):
        """
        Test the endpoint to update a post.

        Args:
            post_response (tuple): A tuple containing the payload, response, and user.
            api_client (APIClient): The API client used to make the request.

        """
        payload, response = post_response
        user, headers = get_user
        title = "Typescript"
        response = api_client().patch(
            f"{self.endpoint}{response.data['slug']}/",
            {"title": title},
            format="json",
            headers=headers,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == title

    def test_delete_post(self, post_response, get_user, api_client):
        """
        Test the endpoint to delete a post.

        Args:
            post_response (tuple): A tuple containing the payload, response, and user.
            api_client (APIClient): The API client used to make the request.

        """
        payload, response = post_response
        user, headers = get_user
        response = api_client().delete(
            f"{self.endpoint}{response.data['slug']}/", headers=headers, format="json"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_like_post(self, post_response, get_user, api_client):
        """
        Test method to verify liking a post.

        Args:
            post_response (tuple): A tuple containing the payload and response for creating a post.
            get_user (tuple): A tuple containing the user information and headers.
            api_client (function): A function that returns an instance of the API client.

        Returns:
            None

        Raises:
            AssertionError: If the response status codes are not HTTP_200_OK or if the number of likes on the post is not at least 1.

        """
        _, response = post_response
        _, headers = get_user
        response_like = api_client().get(
            f"{self.endpoint}like/{response.data['slug']}/",
            headers=headers,
            format="json",
        )
        response_post = api_client().get(
            f"{self.endpoint}{response.data['slug']}/", format="json"
        )
        assert response_post.status_code == status.HTTP_200_OK
        assert response_like.status_code == status.HTTP_200_OK
        assert len(response_post.data["likes"]) >= 1
