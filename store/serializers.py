from decimal import Decimal

from rest_framework import serializers

from store.models import Product, Collection, Review, Cart, CartItem


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
        fields = ('id', 'name', 'description', 'date')

    def create(self, validated_data):
        product_pk = self.context.get('product_pk')
        return Review.objects.create(product_id=product_pk, **validated_data)


class ProductCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'unit_price', 'inventory')


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('cart_id', 'product', 'quantity', 'total_price')

    product = ProductCartItemSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    @staticmethod
    def get_total_price(obj: CartItem):
        return obj.quantity * obj.product.unit_price


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('uuid', 'items', 'total_price')

    uuid = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    @staticmethod
    def get_total_price(obj: Cart):
        return sum(item.quantity * item.product.unit_price for item in obj.items.all())
