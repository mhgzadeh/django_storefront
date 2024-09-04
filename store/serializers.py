from decimal import Decimal

from rest_framework import serializers

from store.models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'title')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'unit_price', 'price_with_tax', 'collection', 'collection_string',
                  'collection_obj', 'collection_hyperlink')

    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax')
    collection_string = serializers.StringRelatedField(source='collection')
    collection_obj = CollectionSerializer(source='collection')
    collection_hyperlink = serializers.HyperlinkedRelatedField(queryset=Collection.objects.all(), source='collection',
                                                               view_name='collection_detail')

    @staticmethod
    def get_price_with_tax(obj: Product):
        return obj.unit_price * Decimal(1.1)
