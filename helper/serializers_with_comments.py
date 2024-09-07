# from decimal import Decimal
#
# from rest_framework import serializers
#
# from store.models import Product, Collection
#
#
# class CollectionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Collection
#         fields = ('id', 'title', 'products_count')
#
#     # just 3 hits to the database
#     products_count = serializers.IntegerField(read_only=True)
#
#     # one hit per each collection to database
#     # product_count = serializers.SerializerMethodField(method_name='get_product_count')
#     # @staticmethod
#     # def get_product_count(obj: Collection):
#     #     return obj.products.count()
#
#
# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ('id', 'title', 'slug', 'description', 'inventory', 'unit_price', 'price_with_tax', 'collection')
#
#     price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax', read_only=True)
#
#     @staticmethod
#     def get_price_with_tax(obj: Product):
#         return obj.unit_price * Decimal(1.1)
#
# # collection = CollectionSerializer() # collection_string = serializers.StringRelatedField(source='collection') #
# collection_hyperlink = serializers.HyperlinkedRelatedField(queryset=Collection.objects.all(), source='collection',
#                                                            view_name='collection_detail')
