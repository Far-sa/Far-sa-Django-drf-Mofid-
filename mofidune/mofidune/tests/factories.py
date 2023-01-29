import factory

from mofidune.product.models import (
    Attribute,
    AttributeValue,
    Category,
    Product,
    ProductImage,
    ProductLine,
    ProductLineAttributeValue,
    ProductType,
)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    # name = "test_category"
    name = factory.Sequence(lambda n: "test_category_%d" % n)
    slug = factory.sequence(lambda n: "test_slug_%d" % n)


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    name = factory.Sequence(lambda n: "test_type_name_%d" % n)

    # @factory.post_generation
    # def attribute(self, create, extracted, **kwargs):
    #     if not create or not extracted:
    #         return self.attribute.add(*extracted)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: "test_product_name_%d" % n)
    pid = factory.Sequence(lambda n: "0000_%d" % n)
    description = "test_description"
    is_digital = False
    is_active = True
    category = factory.SubFactory(CategoryFactory)
    product_type = factory.SubFactory(ProductTypeFactory)


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = 10.00
    sku = "12345"
    stock_qty = 1
    product = factory.SubFactory(ProductFactory)
    is_active = True
    order = "1"
    weight = 100
    product_type = factory.SubFactory(ProductTypeFactory)


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    alternative_text = "test alternative test"
    url = "test.jpg"
    product_line = factory.SubFactory(ProductLineFactory)


class AttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attribute

    name = "attribute_name_test"
    description = "attribute_description_test"


class AttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeValue

    attribute_value = "attr_test"
    attribute = factory.SubFactory(AttributeFactory)


class ProductLineAttributeValues(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLineAttributeValue

    attribute_value = factory.SubFactory(AttributeValueFactory)
    product_line = factory.SubFactory(ProductLineFactory)


# class BrandFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Brand

#     name = factory.Sequence(lambda n: "Category_%d" % n)
