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


# !TestTransactionEndpoints
class TestTransactionEndpoints:
    endpoint = "/transactions/"

    def test_return_all_transactions(self, transaction_factory, api_client):
        transaction_factory.create_batch(4)
        response = api_client().get(self.endpoint, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert len(json.loads(response.content)) == 4

    def test_create_transaction(self, transaction_factory, api_client):
        data = {
            "from_user": "0x3c44cdddb6a900fa2b585dd299e03d12fa4293bc",
            "confirmations": 1,
            "value": "35.0",
            "adopted_pet_slug": "rocky",
            "payment_options": "STRIPE",
            "session_id": "cs_test_b1D5D5VWQuuh2C2TwhAOhHjgIpopAyO1N4oH6tdOu9LXHshEIy8pV7rIDr",
        }
        response = api_client().post(
            self.endpoint,
            data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
