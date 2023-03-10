from django.contrib.auth.models import User
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import (Attribute, AttributeValue, Category, Product,
                     ProductImage, ProductLine)


class CategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = ["category", "slug"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ("id", "product_line")


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
    # category = CategorySerializer()
    category_name = serializers.CharField(source="category.name")
    product_line = ProductLineSerializer(many=True)
    attribute = serializers.SerializerMethodField()
    # attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "pid",
            "description",
            # "brand",
            # "category",
            "category_name",
            "product_line",
            "attribute",
        ]

    def get_attribute(self, obj):
        attribute = Attribute.objects.filter(
            product_type_attribute__product_type__id=obj.id
        )
        print("attribute:", attribute)
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


class ProductLineCategorySerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = ["price", "product_image"]


class ProductCategorySerializer(serializers.ModelSerializer):
    product_line = ProductLineCategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ["product_line", "name", "slug", "pid", "created_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        x = data.pop("product_line")

        if x:

            price = x[0]["price"]
            image = x[0]["product_image"]
            data.update({"price": price})
            data.update({"image": image})

        return data


class ProductDetailSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(slug_field="username", queryset=User.objects)
    category = serializers.SerializerMethodField()
    image = Base64ImageField()

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Product
        exclude = "modified"
