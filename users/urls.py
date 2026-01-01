from django.urls import path
from rest_framework.routers import DefaultRouter

from users.views.me_views import MeView
from users.views.popular_users_view_set import PopularUsersViewSet
from users.views.user_register_view_set import UserRegisterViewSet
from users.views.user_view_set import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("users/popular", PopularUsersViewSet, basename="popular-users")

urlpatterns = [
    path("users/me/", MeView.as_view(), name="users-me"),
    path("users/register/", UserRegisterViewSet.as_view({"post": "create"})),
]

urlpatterns += router.urls
