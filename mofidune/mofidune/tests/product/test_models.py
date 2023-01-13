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


class TestProductLineModel:
    def test_str_method(self, product_line_factory):
        obj = product_line_factory(sku="12345")
        assert obj.__str__() == "12345"
