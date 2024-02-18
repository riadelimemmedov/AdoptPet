import json

import pytest

# * If you don't declare pytestmark our test class model don't accsess to database table
pytestmark = pytest.mark.django_db


# !TestPetManagers
class TestPetEndpoints:
    endpoint = "/pets/"

    def test_return_all_pets(self, pet_factory_end_to_end, api_client):
        pet_factory_end_to_end.create_batch(4)
        response = api_client().get(self.endpoint, format="json")

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 4
