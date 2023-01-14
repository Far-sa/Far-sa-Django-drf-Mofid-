from rest_framework import serializers

from .models import (
    Attribute,
    AttributeValue,
    Brand,
    Category,
    Product,
    ProductImage,
    ProductLine,
)


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = ["category_name"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ("id",)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ("id", "productline")


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ["name", "id"]


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = ["attribute", "attribute_value"]


class ProductLineSerializer(serializers.ModelSerializer):
    # Product = ProductSerializer()
    product_image = ProductImageSerializer(many=True)
    attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = [
            "price",
            "sku",
            "stock_qty",
            "order",
            "product_image",
            "attribute_value",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attribute_value")
        attr_values = {}
        for key in av_data:
            attr_values.update({key["attribute"]["name"]: key["attribute_value"]})
        data.update({"specification": attr_values})
        # print(data)
        return data


class ProductSerializer(serializers.ModelSerializer):
    # brand = BrandSerializer()
    brand_name = serializers.CharField(source="brand.name")
    # category = CategorySerializer()
    category_name = serializers.CharField(source="category.name")
    product_line = ProductLineSerializer(many=True)
    attribute = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "description",
            # "brand",
            "brand_name",
            # "category",
            "category_name",
            "product_line",
            "attribute",
        ]

    def get_attribute(self, obj):
        attribute = Attribute.objects.filter(product_type_attribute__product__id=obj.id)
        return AttributeSerializer(attribute, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attribute")
        attr_values = {}
        for key in av_data:
            attr_values.update({key["id"]: key["name"]})
        data.update({"type specification": attr_values})
        # print(data)
        return data


# OrderedDict(
#     [
#         ("price", "10.00"),
#         ("sku", "9131411250"),
#         ("stock_qty", 50),
#         ("order", 1),
#         (
#             "product_image",
#             [
#                 OrderedDict(
#                     [("alternative_text", "1"), ("url", "/test.jpg"), ("order", 1)]
#                 ),
#                 OrderedDict(
#                     [("alternative_text", "2"), ("url", "/test.jpg"), ("order", 2)]
#                 ),
#             ],
#         ),
#         (
#             "attribute_value",
#             [
#                 OrderedDict(
#                     [
#                         ("attribute", OrderedDict([("name", "size"), ("id", 4)])),
#                         ("attribute_value", "1-kg"),
#                     ]
#                 ),
#                 OrderedDict(
#                     [
#                         ("attribute", OrderedDict([("name", "size"), ("id", 4)])),
#                         ("attribute_value", "3-kg"),
#                     ]
#                 ),
#                 OrderedDict(
#                     [
#                         ("attribute", OrderedDict([("name", "size"), ("id", 4)])),
#                         ("attribute_value", "5-kg"),
#                     ]
#                 ),
#                 OrderedDict(
#                     [
#                         ("attribute", OrderedDict([("name", "flavour"), ("id", 3)])),
#                         ("attribute_value", "coconut"),
#                     ]
#                 ),
#                 OrderedDict(
#                     [
#                         ("attribute", OrderedDict([("name", "flavour"), ("id", 3)])),
#                         ("attribute_value", "oat"),
#                     ]
#                 ),
#                 OrderedDict(
#                     [
#                         ("attribute", OrderedDict([("name", "flavour"), ("id", 3)])),
#                         ("attribute_value", "seeds"),
#                     ]
#                 ),
#             ],
#         ),
#     ]
# )


# OrderedDict(
#     [
#         ("price", "200.00"),
#         ("sku", "9131416245"),
#         ("stock_qty", 5),
#         ("order", 1),
#         (
#             "product_image",
#             [
#                 OrderedDict(
#                     [("alternative_text", "1"), ("url", "/test.jpg"), ("order", 1)]
#                 ),
#                 OrderedDict(
#                     [("alternative_text", "2"), ("url", "/test.jpg"), ("order", 2)]
#                 ),
#                 OrderedDict(
#                     [("alternative_text", "3"), ("url", "/test.jpg"), ("order", 3)]
#                 ),
#             ],
#         ),
#         (
#             "attribute_value",
#             [
#                 OrderedDict(
#                     [
#                         ("attribute", OrderedDict([("name", "color"), ("id", 1)])),
#                         ("attribute_value", "black"),
#                     ]
#                 ),
#                 OrderedDict(
#                     [
#                         ("attribute", OrderedDict([("name", "hard"), ("id", 2)])),
#                         ("attribute_value", "64"),
#                     ]
#                 ),
#             ],
#         ),
#     ]
# )
