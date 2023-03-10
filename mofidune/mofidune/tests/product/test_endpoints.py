import json

import factory
import pytest

pytestmark = pytest.mark.django_db


# class TestCategoryEndpoint:

#     endpoint = "/api/category/"

#     def test_category_get(self, category_factory, api_client):
#         #! Arrange
#         category_factory.create_batch(4)
#         #! Act
#         response = api_client().get(self.endpoint)
#         #! Assert
#         assert response.status_code == 200
#         assert len(json.loads(response.content)) == 4


# class TestBrandEndpoint:

#     endpoint = "/api/brand/"

#     def test_brand_get(self, brand_factory, api_client):
#         #! Arrange
#         brand_factory.create_batch(4)
#         #! Act
#         response = api_client().get(self.endpoint)
#         #! Assert
#         assert response.status_code == 200
#         assert len(json.loads(response.content))


class TestProductEndpoint:

    endpoint = "/api/product/"

    def test_return_single_product(self, product_factory, api_client):
        #! Arrange
        product_factory.create_batch(4)
        #! Act
        response = api_client().get(self.endpoint)
        #! Assert
        assert response.status_code == 200
        assert len(json.loads(response.content))

    def test_return_single_product_by_slug(self, product_factory, api_client):
        obj = product_factory(slug="test-slug")
        response = api_client().get(f"{self.endpoint}{obj.slug}/")
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    # def test_return_product_by_category_slug(
    #     self, product_factory, category_factory, api_client
    # ):
    #     obj = category_factory(slug="test-slug")
    #     product_factory(category=obj)
    #     response = api_client().get(f"{self.endpoint}category/{obj.slug}/")
    #     assert response.status_code == 200
    #     assert len(json.loads(response.content)) == 1
