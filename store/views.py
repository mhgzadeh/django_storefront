from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from store.filters import ProductFilter
from store.models import Product, Collection, Review, Cart, CartItem, Customer, Order, ProductImage
from store.pagination import DefaultPagination
from store.permissions import IsAdminOrReadOnly, FullDjangoModelPermissions, ViewCustomerHistoryPermissions
from store.serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, \
    CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CustomerSerializer, OrderSerializer, \
    CreateOrderSerializer, UpdateOrderSerializer, ProductImageSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('title', 'description', 'collection__title')
    ordering_fields = ('unit_price', 'last_update')

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.items.count() > 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        product.delete()
        return Response(data={'success': f'Successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['product_id'] = self.kwargs['product_pk']
        return context

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def destroy(self, request, *args, **kwargs):
        collection = self.get_object()
        if collection.products.count() > 0:
            return Response(data={'error': 'Collection cannot be deleted because it has been associated with an item.'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_pk': self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    lookup_field = 'uuid'


class CartItemViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_uuid']).select_related('product')

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_uuid']}


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsAdminUser, FullDjangoModelPermissions)

    @action(detail=True, permission_classes=(ViewCustomerHistoryPermissions,))
    def history(self, request, pk):
        return Response(f'{request.user.first_name} {request.user.last_name} {pk}')

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=(IsAuthenticated,))
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()

        customer = Customer.objects.only('id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer.id)
