from rest_framework import serializers

from .models import Brand, Category, Product, ProductLine


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = ["category_name"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ("id",)


class ProductLineSerializer(serializers.ModelSerializer):
    # Product = ProductSerializer()

    class Meta:
        model = ProductLine
        exclude = (
            "id",
            "product",
        )


class ProductSerializer(serializers.ModelSerializer):
    # brand = BrandSerializer()
    brand_name = serializers.CharField(source="brand.name")
    # category = CategorySerializer()
    category_name = serializers.CharField(source="category.name")
    product_line = ProductLineSerializer(many=True)

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
        ]
