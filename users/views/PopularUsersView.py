from django.db.models import Count
from rest_framework.viewsets import ReadOnlyModelViewSet

from users.models import User
from users.serializers.userSerializer import UserSerializer


class PopularUsersViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.annotate(
            followers_count=Count("followers", distinct=True),
            posts_count=Count("posts", distinct=True),
        ).order_by("-followers_count", "-posts_count")
