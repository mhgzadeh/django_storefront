# from django.db.models import Count
# from rest_framework import status
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.response import Response
#
# from store.models import Product, Collection
# from store.serializers import ProductSerializer, CollectionSerializer
#
#
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('collection').all().order_by('-id')
#     serializer_class = ProductSerializer
#
#
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#     def delete(self, request, *args, **kwargs):
#         product = Product.objects.get(pk=self.kwargs['pk'])
#         if product.items.count() > 0:
#             return Response(data={'error: Product cannot be deleted because it has been associated with an order .'},
#                             status=status.HTTP_406_NOT_ACCEPTABLE)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all().order_by('-id')
#     serializer_class = CollectionSerializer
#
#
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all().order_by('-id')
#     serializer_class = CollectionSerializer
#
#     def delete(self, request, *args, **kwargs):
#         collection = Collection.objects.get(pk=self.kwargs['pk'])
#         if collection.products.count() > 0:
#             return Response(data={'error: Collection cannot be deleted because it has been associated with an order .'},
#                             status=status.HTTP_406_NOT_ACCEPTABLE)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
