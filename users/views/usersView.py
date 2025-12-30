from django.db.models import Count, Exists, OuterRef
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from follows.models import Follow
from users.models import User
from users.serializers.ChangePasswordSerializer import ChangePasswordSerializer
from users.serializers.userSerializer import UserSerializer
from users.serializers.userUpdateSerializer import UserUpdateSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "email", "user_tag", "full_name"]

    lookup_field = "username"
    lookup_url_kwarg = "username"

    http_method_names = ["get", "patch", "post", "delete", "head", "options"]

    def get_queryset(self):
        user = self.request.user

        queryset = User.objects.all().annotate(
            followers_count=Count("followers", distinct=True),
            following_count=Count("following", distinct=True),
        )

        # 👇 Otimiza is_following / is_follower
        if user.is_authenticated:
            queryset = queryset.annotate(
                is_following=Exists(
                    Follow.objects.filter(
                        follower=user,
                        following=OuterRef("pk"),
                    )
                ),
                is_follower=Exists(
                    Follow.objects.filter(
                        follower=OuterRef("pk"),
                        following=user,
                    )
                ),
            )

        return queryset

    @action(detail=False, methods=["get", "patch"], url_path="me")
    def me(self, request):
        user = self.get_queryset().get(pk=request.user.pk)

        if request.method == "PATCH":
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(UserSerializer(user, context={"request": request}).data)

    @action(
        detail=False,
        methods=["patch"],
        permission_classes=[IsAuthenticated],
        url_path="me/change-password",
    )
    def change_password(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"detail": "Senha alterada com sucesso."},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
        url_path="follow",
    )
    def follow_toggle(self, request, username=None):
        target_user = get_object_or_404(User, username=username)
        current_user = request.user

        if target_user == current_user:
            return Response(
                {"detail": "Você não pode seguir a si mesmo."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow = Follow.objects.filter(
            follower=current_user,
            following=target_user,
        ).first()

        # 👉 SEGUIR
        if request.method == "POST":
            if follow:
                return Response(
                    {"detail": "Você já segue este usuário."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            Follow.objects.create(
                follower=current_user,
                following=target_user,
            )

            return Response(
                {"detail": "Usuário seguido com sucesso."},
                status=status.HTTP_201_CREATED,
            )

        # 👉 DEIXAR DE SEGUIR
        if request.method == "DELETE":
            if not follow:
                return Response(
                    {"detail": "Você não segue este usuário."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            follow.delete()

            return Response(
                {"detail": "Você deixou de seguir este usuário."},
                status=status.HTTP_204_NO_CONTENT,
            )
