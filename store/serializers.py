from decimal import Decimal

from rest_framework import serializers

from store.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'unit_price', 'price_with_tax')

    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax')

    @staticmethod
    def get_price_with_tax(obj: Product):
        return obj.unit_price * Decimal(1.1)
