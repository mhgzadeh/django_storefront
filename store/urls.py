from rest_framework_nested import routers

from store.views import CollectionViewSet, ProductViewSet, ReviewViewSet, CartViewSet, CartItemViewSet, CustomerViewSet, \
    OrderViewSet

router = routers.DefaultRouter()
router.register(prefix='products', viewset=ProductViewSet, basename='products')
router.register(prefix='collections', viewset=CollectionViewSet, basename='collections')
router.register(prefix='carts', viewset=CartViewSet, basename='carts')
router.register(prefix='customers', viewset=CustomerViewSet, basename='customers')
router.register(prefix='orders', viewset=OrderViewSet, basename='orders')

product_routers = routers.NestedDefaultRouter(router, parent_prefix='products', lookup='product')
product_routers.register(prefix='reviews', viewset=ReviewViewSet, basename='product-reviews')

cart_routers = routers.NestedDefaultRouter(router, parent_prefix='carts', lookup='cart')
cart_routers.register(prefix='items', viewset=CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + product_routers.urls + cart_routers.urls
