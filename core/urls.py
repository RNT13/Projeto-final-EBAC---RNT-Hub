from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from api.views import BookViewSet

router = DefaultRouter()
router.register(r"books", BookViewSet, basename="books")


def api_root(request):
    return JsonResponse(
        {
            "status": "ok",
            "message": "Bem-vindo(a) à API do projeto RNT-Hub",
            "version": "v1",
            "links": {
                "books": "/api/v1/books/",
            },
        }
    )


urlpatterns = [
    path("", api_root),
    path("admin/", admin.site.urls),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("api/v1/", include(router.urls)),
]
