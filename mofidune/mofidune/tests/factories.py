import factory

from mofidune.product.models import Brand, Category, Product, ProductLine


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    # name = "test_category"
    name = factory.Sequence(lambda n: "test_category_%d" % n)
    slug = factory.sequence(lambda n: "test_slug_%d" % n)


# class BrandFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Brand

#     name = factory.Sequence(lambda n: "Category_%d" % n)


# class ProductFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Product

#     name = "test_product"
#     description = "test_description"
#     is_digital = True
#     brand = factory.SubFactory(BrandFactory)
#     category = factory.SubFactory(CategoryFactory)


# class ProductLineFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = ProductLine

#     price = 10.00
#     sku = "12345"
#     stock_qty = 1
#     product = factory.SubFactory(ProductFactory)
#     is_active = True
#     order = "1"
