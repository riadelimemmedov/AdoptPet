import factories
import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

# Register UserFactork for create fake data
register(factories.UserFactory)


# !api_client
@pytest.fixture
def api_client():
    return APIClient
