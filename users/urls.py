from django.urls import path
from rest_framework.routers import DefaultRouter

from users.views.popular_users_view_set import PopularUsersViewSet
from users.views.user_register_view_set import UserRegisterViewSet
from users.views.user_view_set import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("users/popular", PopularUsersViewSet, basename="popular-users")

urlpatterns = [
    path(
        "register/",
        UserRegisterViewSet.as_view({"post": "create"}),
        name="register",
    ),
]

urlpatterns += router.urls
