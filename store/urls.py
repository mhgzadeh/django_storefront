from django.urls import path

from store.views import CollectionDetail, CollectionList, ProductDetail, ProductList

urlpatterns = [
    path('collections/', CollectionList.as_view(), name='collection_list'),
    path('collections/<int:pk>/', CollectionDetail.as_view(), name='collection_detail'),
    path('products/', ProductList.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
]
