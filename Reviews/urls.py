from rest_framework.routers import DefaultRouter
from .views import ReviewView

router = DefaultRouter()
router.register(f'review', ReviewView)
urlpatterns = router.urls
