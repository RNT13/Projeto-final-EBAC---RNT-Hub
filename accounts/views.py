from rest_framework import mixins, permissions, viewsets

from .models import User
from .serializers import UserRegisterSerializer, UserSerializer
from rest_framework.permissions import AllowAny


# -------------------------------------------------------------------
#   1. Registro de usuário (somente CREATE)
# -------------------------------------------------------------------
class UserRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


# -------------------------------------------------------------------
#   2. Perfil do usuário logado (GET e UPDATE)
# -------------------------------------------------------------------
class UserMeViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# -------------------------------------------------------------------
#   3. Listar usuários
# -------------------------------------------------------------------
class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
