from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views.me_views import MeView
from users.views.popular_users_view_set import PopularUsersViewSet
from users.views.user_register_view_set import UserRegisterViewSet
from users.views.user_view_set import UserViewSet

router = DefaultRouter()
router.register("", UserViewSet, basename="users")
router.register("popular-users", PopularUsersViewSet, basename="popular-users")

urlpatterns = [
    path("me/", MeView.as_view(), name="users-me"),
    path("register/", UserRegisterViewSet.as_view({"post": "create"})),
    path("", include(router.urls)),
]

urlpatterns += router.urls
