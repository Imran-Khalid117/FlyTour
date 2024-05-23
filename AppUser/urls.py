from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from AppUser.views import PublicUserViewSet

router = DefaultRouter()
router.register(f'user', PublicUserViewSet)
urlpatterns = [
    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
