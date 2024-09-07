from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from store.models import Product, Collection
from store.serializers import ProductSerializer, CollectionSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

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
