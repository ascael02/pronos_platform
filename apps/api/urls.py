"""
Routes API REST v1.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import PronosticViewSet, SportViewSet, BookmakerViewSet, ArticleViewSet

router = DefaultRouter()
router.register(r'pronostics', PronosticViewSet, basename='pronostic')
router.register(r'sports', SportViewSet, basename='sport')
router.register(r'bookmakers', BookmakerViewSet, basename='bookmaker')
router.register(r'articles', ArticleViewSet, basename='article')

urlpatterns = [
    path('', include(router.urls)),
    # JWT Auth
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
