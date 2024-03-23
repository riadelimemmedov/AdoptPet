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


# !TestOrderEndpoints
class TestOrderEndpoints:
    endpoint = "/orders/create-checkout-session/"

    def test_create_order(self, api_client):
        """
        Test the creation of an order using the provided API client.

        Args:
            self: The instance of the test case.
            api_client: The API client used to make the HTTP request.

        Returns:
            None

        Raises:
            AssertionError: If the response status code is not HTTP 201 (Created).

        """
        data = b'{"pets":[[{"type":"BigNumber","hex":"0x02"},"rocky","Rocky","#FF29C4",{"type":"BigNumber","hex":"0x23"},"https://images.unsplash.com/photo-1537019575197-df34a13f342c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1338&q=40"],[{"type":"BigNumber","hex":"0x01"},"frieda","Frieda","#D92DFF",{"type":"BigNumber","hex":"0x20"},"https://images.unsplash.com/photo-1600682011352-e448301668e7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1348&q=40"]],"from_user":"0x3c44cdddb6a900fa2b585dd299e03d12fa4293bc"}'
        response = api_client().post(
            self.endpoint,
            data=data,
            content_type="application/json",
        )
        assert (
            response.status_code == status.HTTP_201_CREATED
            or response.status_code == status.HTTP_200_OK
        )
