from django.urls import path
from rest_framework.routers import DefaultRouter

from users.views.PopularUsersView import PopularUsersViewSet
from users.views.registerView import UserRegisterViewSet
from users.views.usersView import UserViewSet

router = DefaultRouter()
router.register("", UserViewSet, basename="users")
router.register("popular", PopularUsersViewSet, basename="popular-users")

urlpatterns = [
    path(
        "register/",
        UserRegisterViewSet.as_view({"post": "create"}),
        name="register",
    ),
]

urlpatterns += router.urls
