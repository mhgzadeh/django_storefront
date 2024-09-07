from rest_framework.routers import SimpleRouter

from store.views import CollectionViewSet, ProductViewSet

router = SimpleRouter()
router.register(prefix='products', viewset=ProductViewSet)
router.register(prefix='collections', viewset=CollectionViewSet)

urlpatterns = router.urls
