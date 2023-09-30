from rest_framework import serializers
from .models import Cart, CartItem
from shop.models import Product


class ProductSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['total_price'], representation['productCount'] = instance.get_count_and_total()

        return representation

    class Meta:
        model = Cart
        fields = ['items']
