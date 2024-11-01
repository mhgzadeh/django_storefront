from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from store.models import Product, Collection, Review, Cart, CartItem, Customer, Order, OrderItem, ProductImage
from store.signals import order_created


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'title', 'products_count')

    products_count = serializers.IntegerField(read_only=True)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')

    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id=product_id, **validated_data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'slug', 'description', 'inventory', 'unit_price', 'price_with_tax', 'collection',
                  'images')

    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

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


class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'unit_price')


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('cart_id', 'product', 'quantity', 'total_price')

    product = CartItemProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    @staticmethod
    def get_total_price(obj: CartItem):
        return obj.quantity * obj.product.unit_price


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('cart_id', 'product_id', 'quantity')

    product_id = serializers.IntegerField()

    @staticmethod
    def validate_product_id(value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('Product does not exist')
        return value

    def save(self):
        cart_id = self.context.get('cart_id')
        product_id = self.validated_data.get('product_id')
        quantity = self.validated_data.get('quantity')
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('quantity',)


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


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'phone', 'birth_date', 'membership', 'user_id')


class OrderItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'unit_price', 'inventory')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'order_id', 'product', 'quantity', 'unit_price')

    order_id = serializers.IntegerField()
    product = OrderItemProductSerializer()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'placed_at', 'payment_status', 'customer', 'items')

    items = OrderItemSerializer(many=True)
    customer = CustomerSerializer()


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('payment_status',)


class CreateOrderSerializer(serializers.Serializer):
    cart_uuid = serializers.UUIDField()

    @staticmethod
    def validate_cart_uuid(cart_uuid):
        if not Cart.objects.filter(uuid=cart_uuid).exists():
            raise serializers.ValidationError('Cart does not exist.')
        if CartItem.objects.filter(cart_id=cart_uuid).count() == 0:
            raise serializers.ValidationError('The cart has no items.')
        return cart_uuid

    def save(self, **kwargs):
        with transaction.atomic():
            customer = Customer.objects.get(user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects.select_related('product').filter(cart_id=self.validated_data['cart_uuid'])

            order_items = [
                OrderItem(order=order, product=item.product, unit_price=item.product.unit_price, quantity=item.quantity)
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(uuid=self.validated_data['cart_uuid']).delete()

            order_created.send_robust(self.__class__, order=order)

            return order
