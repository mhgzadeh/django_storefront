from decimal import Decimal

from rest_framework import serializers

from store.models import Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'title', 'products_count')

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'slug', 'description', 'inventory', 'unit_price', 'price_with_tax', 'collection')

    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax', read_only=True)

    @staticmethod
    def get_price_with_tax(obj: Product):
        return obj.unit_price * Decimal(1.1)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'date', 'name', 'description', 'product')
