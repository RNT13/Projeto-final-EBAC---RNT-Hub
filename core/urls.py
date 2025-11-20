from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from accounts.views import AccountViewSet, UserMeViewSet, UserRegisterViewSet
from feed.views import FeedViewSet
from follows.views import FollowViewSet
from likes.views import LikeViewSet
from notifications.views import NotificationViewSet
from posts.views import PostViewSet

router = DefaultRouter()

# Accounts
router.register(r"accounts/register", UserRegisterViewSet, basename="register")
router.register(r"accounts/me", UserMeViewSet, basename="me")
router.register(r"accounts", AccountViewSet, basename="accounts")

# Posts, Likes, Follows, Notifications
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"likes", LikeViewSet, basename="likes")
router.register(r"follows", FollowViewSet, basename="follows")
router.register(r"notifications", NotificationViewSet, basename="notifications")


def api_root(request):
    return JsonResponse(
        {
            "status": "ok",
            "message": "Bem-vindo(a) à API do projeto RNT-Hub",
            "version": "v1",
            "links": {
                "admin": "/admin/",
                "token": "/api/token/",
                "books": "/api/v1/books/",
                "accounts": "/api/v1/accounts/",
                "me": "/api/v1/accounts/me/",
                "register": "/api/v1/accounts/register/",
                "posts": "/api/v1/posts/",
                "comments": "/api/v1/posts/<id>/comments/",
                "likes": "/api/v1/likes/",
                "follows": "/api/v1/follows/",
                "notifications": "/api/v1/notifications/",
                "feed_user": "/api/v1/feed/user/",
                "feed_explore": "/api/v1/feed/explore/",
                "feed_images": "/api/v1/feed/images/",
                "feed_algorithm": "/api/v1/feed/algorithm/",
            },
        }
    )


feed = FeedViewSet.as_view

urlpatterns = [
    path("", api_root),
    path("admin/", admin.site.urls),
    path("api/token/", obtain_auth_token, name="token"),
    path("api/v1/", include(router.urls)),
    # Feeds
    path("api/v1/feed/user/", feed({"get": "user_feed"}), name="feed-user"),
    path("api/v1/feed/explore/", feed({"get": "explore_feed"}), name="feed-explore"),
    path("api/v1/feed/images/", feed({"get": "images_feed"}), name="feed-images"),
    path("api/v1/feed/algorithm/", feed({"get": "algorithm_feed"}), name="feed-algorithm"),
]
