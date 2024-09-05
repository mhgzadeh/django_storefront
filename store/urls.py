from django.urls import path

from store.views import ProductList, ProductDetail, collection_detail, collection_list

urlpatterns = [
    path('products/', ProductList.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('collections/', collection_list, name='collection_list'),
    path('collections/<int:pk>/', collection_detail, name='collection_detail'),
]
