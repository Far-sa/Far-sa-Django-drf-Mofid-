import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from mofidune.product.models import Category, Product, ProductLine

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
        product_factory(category=obj1)
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


class TestProductLineModel:
    def test_str_method(self, product_line_factory):
        obj = product_line_factory(sku="12345")
        assert obj.__str__() == "12345"

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(order=1, product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj).clean()

    def test_field_decimal_places(self, product_line_factory):
        price = 1.001
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_field_price_max_digits(self, product_line_factory):
        price = 1000.00
        with pytest.raises(ValidationError):
            product_line_factory(price=price)

    def test_field_sku_max_length(self, product_line_factory):
        sku = "x" * 11
        with pytest.raises(ValidationError):
            product_line_factory(sku=sku)

    def test_fk_product_on_delete_protect(self, product_line_factory, product_factory):
        obj1 = product_factory()
        product_line_factory(product=obj1)
        with pytest.raises(IntegrityError):
            obj1.delete()

    # def test_return_product_active_only_true(self, product_line_factory):
    #     product_line_factory(is_active=True)
    #     product_line_factory(is_active=False)
    #     qs = ProductLine.objects.is_active().count
    #     assert qs == 1

    def test_return_product_active_only_false(self, product_line_factory):
        product_line_factory(is_active=True)
        product_line_factory(is_active=False)
        qs = ProductLine.objects.count()
        assert qs == 2


class TestProductImageModel:
    def test_str_method(self, product_image_factory, product_line_factory):
        obj1 = product_line_factory(sku="12345")
        obj2 = product_image_factory(order=1, product_line=obj1)
        assert obj2.__str__() == "12345_img"


class TestProductTypeModel:
    def test_str_method(self, product_type_factory):
        obj = product_type_factory(name="test_product")
        assert obj.__str__() == "test_product"


# class TestBrandModel:
#     def test_str_method(self, brand_factory):
#         # AAA
#         obj = brand_factory(name="test_brand")
#         assert obj.__str__() == "test_brand"


# class TestProductLineModel:
#     def test_str_method(self, product_line_factory):
#         obj = product_line_factory(sku="12345")
#         assert obj.__str__() == "12345"
