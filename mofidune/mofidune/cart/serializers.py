from rest_framework import serializers

from mofidune.product.models import Product

from .models import Cart, CartItem


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "title",
            "seller",
            "quantity",
            "price",
            "image",
        )


class CartItemSerializer(serializers.ModelSerializer):
    # product = CartProductSerializer(required=False)
    class Meta:
        model = CartItem
        fields = ["cart", "product", "quantity"]


class CartItemMiniSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(required=False)

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["product", "quantity"]
