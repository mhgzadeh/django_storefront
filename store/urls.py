from rest_framework_nested import routers

from store.views import CollectionViewSet, ProductViewSet, ReviewViewSet, CartViewSet

router = routers.DefaultRouter()
router.register(prefix='products', viewset=ProductViewSet, basename='products')
router.register(prefix='collections', viewset=CollectionViewSet, basename='collections')
router.register(prefix='carts', viewset=CartViewSet, basename='carts')

product_routers = routers.NestedDefaultRouter(router, parent_prefix='products', lookup='product')
product_routers.register(prefix='reviews', viewset=ReviewViewSet, basename='product-reviews')

urlpatterns = router.urls + product_routers.urls
