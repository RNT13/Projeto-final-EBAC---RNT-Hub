# users/views/usersView.py
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User
from users.serializers.userSerializer import UserSerializer
from users.serializers.userUpdateSerializer import UserUpdateSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    http_method_names = ["get", "patch", "head", "options"]

    @action(detail=False, methods=["get", "patch"], url_path="me")
    def me(self, request):
        user = request.user

        if request.method == "GET":
            return Response(UserSerializer(user).data)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(UserSerializer(user).data)
