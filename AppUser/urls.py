from rest_framework.routers import DefaultRouter
from AppUser.views import PublicUserViewSet

router = DefaultRouter()
router.register(f'user', PublicUserViewSet)
urlpatterns = router.urls
