import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from mofidune.product.models import Category, Product

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

    def test_name_max_length(self, category_factory):
        name = "x" * 236
        obj = category_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_slug_max_length(self, category_factory):
        slug = "x" * 256
        obj = category_factory(slug=slug)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_name_unique_field(self, category_factory):
        category_factory(name="test_cat")
        with pytest.raises(IntegrityError):
            category_factory(name="test_cat")

    def test_slug_unique_field(self, category_factory):
        category_factory(slug="test_name")
        with pytest.raises(IntegrityError):
            category_factory(slug="test_name")

    def test_is_active_false_default(self, category_factory):
        obj = category_factory()
        assert obj.is_active is False

    def test_return_category_active_only_false(self, category_factory):
        category_factory(is_active=True)
        category_factory(is_active=False)
        qs = Category.objects.count()
        assert qs == 2


class TestProductModel:
    def test_str_method(self, product_factory):
        # AAA
        obj = product_factory(name="test_product")
        assert obj.__str__() == "test_product"

    def test_name_max_length(self, product_factory):
        name = "x" * 236
        obj = product_factory(name=name)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_slug_max_length(self, product_factory):
        slug = "x" * 256
        obj = product_factory(slug=slug)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_pid_length(self, product_factory):
        pid = "x" * 11
        obj = product_factory(pid=pid)
        with pytest.raises(ValidationError):
            obj.full_clean()

    def test_is_digital_false(self, product_factory):
        obj = product_factory(is_digital=False)
        assert obj.is_digital is False

    def test_fk_category_on_delete_protect(self, product_factory, category_factory):
        obj1 = category_factory()
        product_factory(Category=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    # def test_return_product_active_only_true(self, product_factory):
    #     product_factory(is_active=True)
    #     product_factory(is_active=False)
    #     qs = Product.objects.is_active().count()
    #     assert qs == 1

    def test_return_product_active_only_false(self, product_factory):
        product_factory(is_active=True)
        product_factory(is_active=False)
        qs = Product.objects.count()
        assert qs == 2


# def test_return_category_active_only_true(self, category_factory):
#     category_factory(is_active=False)
#     category_factory(is_active=True)
#     qs = Category.objects.is_active().count()
#     assert qs == 1


# class TestBrandModel:
#     def test_str_method(self, brand_factory):
#         # AAA
#         obj = brand_factory(name="test_brand")
#         assert obj.__str__() == "test_brand"


# class TestProductLineModel:
#     def test_str_method(self, product_line_factory):
#         obj = product_line_factory(sku="12345")
#         assert obj.__str__() == "12345"
