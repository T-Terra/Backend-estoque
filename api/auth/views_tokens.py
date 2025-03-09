from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import viewsets, status


"""ViewSet que cuida da criação de tokens JWT"""


class AuthenticationJwt(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        """
        Endpoint para autenticação e geração de JWT.
        """
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"detail": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
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
            refresh_token = str(refresh)

            res = Response({"message": "Login successful"})
            res.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="Strict",
                max_age=3600,  # 1 hora de expiração
            )
            res.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="Strict",
                max_age=3600 * 24,  # 1 dia de expiração
            )

            return res
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AuthJwtRefreshToken(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        refresh_token = request.data.get("refreshtoken")

        if not refresh_token:
            return Response(
                {"datail": "refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            old_refresh = RefreshToken(refresh_token)

            user_id = old_refresh.payload.get("user_id")

            if not user_id:
                return Response(
                    {"detail": "Invalid token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response(
                    {"detail": "User not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            new_token = RefreshToken.for_user(user)

            # Revoga o Refreshtoken antigo
            old_refresh.blacklist()

            return Response(
                {
                    "access": str(new_token.access_token),
                    "refresh": str(new_token),
                },
                status=status.HTTP_200_OK,
            )
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AuthRegister(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        try:
            username = request.data.get("username")
            email = request.data.get("email")
            password = request.data.get("password")

            if not username or not email or not password:
                return Response(
                    {"message": "parameters is missing."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                validate_email(email)
            except ValidationError:
                return Response(
                    {"message": "Invalid email format."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if User.objects.filter(email=email).exists():
                return Response(
                    {"message": "Email already registered."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            User.objects.create_user(username, email, password)

            return Response(
                {"message": "User Created with success"},
                status=status.HTTP_201_CREATED,
            )
        except:
            return Response(
                {"message": "Error to create user or user exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AuthLogOut(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        try:
            refresh_token = request.data.get("refreshtoken")

            if not refresh_token:
                return Response(
                    {"detail": "Refresh token é obrigatório."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = RefreshToken(refresh_token)

            token.check_blacklist()

            token.blacklist()

            response = Response(
                {"detail": "Logout realizado com sucesso."},
                status=status.HTTP_200_OK,
            )

            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")

            return response
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
