from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import BookViewSet

router = DefaultRouter()
router.register(r"books", BookViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
