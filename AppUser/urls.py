from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from AppUser.views import PublicUserViewSet

router = DefaultRouter()
router.register(f'user', PublicUserViewSet)
# These are built in JWT views to generate the access and refresh token. We are calling these views
# in the login view.
urlpatterns = [
    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
