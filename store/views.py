from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from store.models import Product, Collection
from store.serializers import ProductSerializer, CollectionSerializer


class ProductList(APIView):
    @staticmethod
    def get(request):
        queryset = Product.objects.select_related('collection').all().order_by('-id')
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    @staticmethod
    def get(request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @staticmethod
    def put(request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.items.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an item.'},
                            status=status.HTTP_400_BAD_REQUEST)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count=Count('products')).all().order_by('-id')
        serializer = CollectionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if collection.products.all().exists():
            return Response({'error': 'Collection cannot be deleted because it is associated with a product. '})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
