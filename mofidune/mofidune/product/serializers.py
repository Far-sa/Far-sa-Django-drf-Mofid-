from rest_framework import serializers

from .models import Brand, Category, Product


class CategorySerilazer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class BrandSerilazer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class ProductSerilazer(serializers.ModelSerializer):
    brand = BrandSerilazer()
    category = CategorySerilazer()

    class Meta:
        model = Product
        fields = "__all__"
