from rest_framework.routers import DefaultRouter
from .views import PlacesView

router = DefaultRouter()
router.register(f'places', PlacesView)
urlpatterns = router.urls
