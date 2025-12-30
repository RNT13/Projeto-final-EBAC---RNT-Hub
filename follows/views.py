from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets
from rest_framework.exceptions import ValidationError

from users.models import User

from .models import Follow
from .serializers import FollowSerializer


class FollowViewSet(viewsets.ModelViewSet):
    """
    CRUD de follows do usuário autenticado
    - list: quem eu sigo
    - create: seguir alguém
    - destroy: deixar de seguir
    """

    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user).select_related("following")

    def perform_create(self, serializer):
        follower = self.request.user
        following = serializer.validated_data["following"]

        if follower == following:
            raise ValidationError({"detail": "Você não pode seguir a si mesmo."})

        if Follow.objects.filter(follower=follower, following=following).exists():
            raise ValidationError({"detail": "Você já segue esse usuário."})

        serializer.save(follower=follower)


class FollowersListView(generics.ListAPIView):
    """
    Lista quem segue um usuário
    """

    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs["user_id"])

        return Follow.objects.filter(following=user).select_related("follower")


class FollowingListView(generics.ListAPIView):
    """
    Lista quem um usuário está seguindo
    """

    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs["user_id"])

        return Follow.objects.filter(follower=user).select_related("following")
