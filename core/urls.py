from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # ---------------------------------------------------------
    # 📘 Documentação da API
    # ---------------------------------------------------------
    # Swagger UI (interface bonita e interativa)
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # Arquivo JSON/YAML do schema gerado pelo DRF-Spectacular
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # Redoc (documentação alternativa)
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # ---------------------------------------------------------
    # Admin
    # ---------------------------------------------------------
    path("admin/", admin.site.urls),
    # ---------------------------------------------------------
    # JWT Authentication
    # ---------------------------------------------------------
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # ---------------------------------------------------------
    # Apps da API
    # ---------------------------------------------------------
    path("api/v1/users/", include("users.urls")),
    path("api/v1/posts/", include("posts.urls")),
    path("api/v1/likes/", include("likes.urls")),
    path("api/v1/follows/", include("follows.urls")),
    path("api/v1/notifications/", include("notifications.urls")),
    path("api/v1/feed/", include("feed.urls")),
]
