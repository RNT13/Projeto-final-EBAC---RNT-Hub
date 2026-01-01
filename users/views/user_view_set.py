from django.db.models import Count, Exists, OuterRef
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from follows.models import Follow
from users.models import User
from users.serializers.change_password_serializer import ChangePasswordSerializer
from users.serializers.user_serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "email", "user_tag", "full_name"]

    lookup_field = "username"
    lookup_url_kwarg = "username"

    def get_queryset(self):
        user = self.request.user

        queryset = User.objects.annotate(
            followers_count=Count("followers", distinct=True),
            following_count=Count("following", distinct=True),
        )

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

    # ---------------------------
    # FOLLOW TOGGLE
    # ---------------------------
    @action(detail=True, methods=["post", "delete"], url_path="follow")
    def follow_toggle(self, request, username=None):
        target_user = self.get_object()
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

        # DELETE
        if not follow:
            return Response(
                {"detail": "Você não segue este usuário."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # ---------------------------
    # FOLLOWERS
    # ---------------------------
    @action(detail=True, methods=["get"])
    def followers(self, request, username=None):
        user = self.get_object()

        followers = User.objects.filter(following__following=user)

        serializer = UserSerializer(
            followers,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    # ---------------------------
    # FOLLOWING
    # ---------------------------
    @action(detail=True, methods=["get"])
    def following(self, request, username=None):
        user = self.get_object()

        following = User.objects.filter(followers__follower=user)

        serializer = UserSerializer(
            following,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)
