from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from store.filters import ProductFilter
from store.models import Product, Collection, Review, Cart
from store.pagination import DefaultPagination
from store.serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ('title', 'description', 'collection__title')
    ordering_fields = ('unit_price', 'last_update')

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.items.count() > 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        product.delete()
        return Response(data={'success': f'Successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

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
