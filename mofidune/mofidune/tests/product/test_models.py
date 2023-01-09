import pytest

#! AAA
# Arrange
# Act
# Assert

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        # AAA
        obj = category_factory(name="test_cat")
        assert obj.__str__() == "test_cat"


class TestBrandModel:
    def test_str_method(self, brand_factory):
        # AAA
        obj = brand_factory(name="test_brand")
        assert obj.__str__() == "test_brand"


class TestProductModel:
    def test_str_method(self, product_factory):
        # AAA
        obj = product_factory(name="test_product")
        assert obj.__str__() == "test_product"
