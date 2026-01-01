from django.db.models import Count, F, IntegerField, OuterRef, Subquery, Value
from django.db.models.functions import Coalesce
from rest_framework.viewsets import ReadOnlyModelViewSet

from posts.models import Post
from users.models import User
from users.serializers.public_serializer import UserPublicSerializer


class PopularUsersViewSet(ReadOnlyModelViewSet):
    serializer_class = UserPublicSerializer

    def get_queryset(self):
        posts_count = Post.objects.filter(author=OuterRef("pk")).values("author").annotate(c=Count("id")).values("c")

        likes_count = Post.objects.filter(author=OuterRef("pk")).annotate(c=Count("likes")).values("c")

        comments_count = Post.objects.filter(author=OuterRef("pk")).annotate(c=Count("comments")).values("c")

        return (
            User.objects.annotate(
                posts_count=Coalesce(Subquery(posts_count, output_field=IntegerField()), Value(0)),
                likes_count=Coalesce(Subquery(likes_count, output_field=IntegerField()), Value(0)),
                comments_count=Coalesce(Subquery(comments_count, output_field=IntegerField()), Value(0)),
                followers_count=Count("followers", distinct=True),
            )
            .annotate(
                popularity_score=F("followers_count") * 3
                + F("likes_count") * 2
                + F("comments_count") * 3
                + F("posts_count")
            )
            .filter(popularity_score__gt=0)
            .order_by("-popularity_score", "-followers_count")
        )
