import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import CategoryFactory, ProductFactory

register(CategoryFactory)
register(ProductFactory)
# register(BrandFactory)
# register(ProductLineFactory)


@pytest.fixture
def api_client():
    return APIClient
