from rest_framework.routers import DefaultRouter
from .views import FavouritesView

router = DefaultRouter()
router.register(r'favourites', FavouritesView)
urlpatterns = router.urls
