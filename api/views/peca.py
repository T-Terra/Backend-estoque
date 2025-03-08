from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import viewsets, status


from ..serializers.serializer import PecaSerializer
from ..models.peca import Peca
from ..auth.permissions import ApiAccessPermission



"""ViewSet que cria todas as actions da api CRUD"""


class PecaViewSet(viewsets.ModelViewSet):
    queryset = Peca.objects.all()
    serializer_class = PecaSerializer
    permission_classes = [ApiAccessPermission, IsAuthenticated]

class AuthenticationJwt(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        """
        Endpoint para autenticação e geração de JWT.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"detail": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise AuthenticationFailed("Invalid credentials.")
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found.")

        # Geração do token
        try:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response(
                {"access": access_token, "refresh": str(refresh)},
                status=status.HTTP_200_OK
            )
        except TokenError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
