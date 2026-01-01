from django.db.models import Count, F
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import CursorPagination

from follows.models import Follow
from posts.models import Post
from posts.serializers import PostSerializer


# CursorPagination para feed infinito
class FeedCursorPagination(CursorPagination):
    page_size = 10
    ordering = "-created_at"


class FeedViewSet(viewsets.ViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FeedCursorPagination

    """
    FeedViewSet com diferentes tipos de feed:
      1. feed do usuário (quem sigo + meus posts)
      2. feed global / explore
      3. feed filtrado (apenas posts com imagem)
      4. feed por algoritmo (score baseado em likes + comentários)
    """

    # 🔥 BASE QUERYSET COM ANNOTATE (ESSENCIAL)
    def base_queryset(self):
        return Post.objects.select_related("author").annotate(
            likes_count=Count("likes", distinct=True),
            comments_count=Count("comments", distinct=True),
        )

    @action(detail=False, methods=["get"])
    def user_feed(self, request):
        following_ids = Follow.objects.filter(follower=request.user).values_list("following_id", flat=True)

        queryset = (
            self.base_queryset().filter(author__in=list(following_ids) + [request.user.id]).order_by("-created_at")
        )

        return self.paginate_and_serialize(request, queryset)

    @action(detail=False, methods=["get"])
    def explore_feed(self, request):
        queryset = self.base_queryset().order_by("-created_at")
        return self.paginate_and_serialize(request, queryset)

    @action(detail=False, methods=["get"])
    def images_feed(self, request):
        following_ids = Follow.objects.filter(follower=request.user).values_list("following_id", flat=True)

        queryset = (
            self.base_queryset()
            .filter(
                author__in=list(following_ids) + [request.user.id],
                image__isnull=False,
            )
            .order_by("-created_at")
        )

        return self.paginate_and_serialize(request, queryset)

    @action(detail=False, methods=["get"])
    def algorithm_feed(self, request):
        following_ids = Follow.objects.filter(follower=request.user).values_list("following_id", flat=True)

        queryset = (
            self.base_queryset()
            .filter(author__in=list(following_ids) + [request.user.id])
            .annotate(score=F("likes_count") * 2 + F("comments_count"))
            .order_by("-score", "-created_at")
        )

        return self.paginate_and_serialize(request, queryset)

    # 🔁 Helper para paginação + serializer
    def paginate_and_serialize(self, request, queryset):
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = PostSerializer(page, many=True, context={"request": request})

        return paginator.get_paginated_response(serializer.data)
