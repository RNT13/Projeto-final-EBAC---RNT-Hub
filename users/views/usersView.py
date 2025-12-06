# users/views/usersView.py
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User
from users.serializers.userSerializer import UserSerializer
from users.serializers.userUpdateSerializer import UserUpdateSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get", "patch"], url_path="me")
    def me(self, request):
        user = request.user

        # ✅ GET -> dados completos (perfil)
        if request.method == "GET":
            return Response(UserSerializer(user).data)

        # ✅ PATCH -> somente campos editáveis
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # ✅ retorna perfil atualizado completo
        return Response(UserSerializer(user).data)
