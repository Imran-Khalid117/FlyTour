from rest_framework.routers import DefaultRouter
from Catagories.views import CategoryViewSet

router = DefaultRouter()
router.register(f'category', CategoryViewSet)
urlpatterns = router.urls
