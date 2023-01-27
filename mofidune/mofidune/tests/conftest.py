import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import (
    CategoryFactory,
    ProductFactory,
    ProductImageFactory,
    ProductLineFactory,
    ProductTypeFactory,
)

register(CategoryFactory)
register(ProductFactory)
register(ProductLineFactory)
register(ProductImageFactory)
register(ProductTypeFactory)
# register(BrandFactory)


@pytest.fixture
def api_client():
    return APIClient
