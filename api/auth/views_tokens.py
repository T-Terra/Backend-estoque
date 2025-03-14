from django.contrib.auth.models import User
from ..models.jwt_access_token import JwtAccessToken
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import viewsets, status
from api.auth.auth_custom import JWTAuthenticationDefault
from datetime import datetime

"""ViewSet que cuida da criação de tokens JWT"""


class AuthenticationJwt(viewsets.ViewSet):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

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
            raise AuthenticationFailed("Invalid credentials.")

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
                samesite="None",  # "Strict"
                max_age=3600,  # 1 hora de expiração
            )
            res.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="None",  # "Strict"
                max_age=3600 * 24,  # 1 dia de expiração
            )

            return res
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AuthJwtRefreshToken(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")
        
        if not refresh_token:
            return Response(
                {"datail": "refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Decodifica os tokens
            old_refresh = RefreshToken(refresh_token)

            old_access = AccessToken(access_token)

            # Pega o timestamp de expiração do access token
            exp_timestamp = old_access['exp']

            exp_datetime = datetime.fromtimestamp(exp_timestamp)

            date_now = datetime.now()

            if exp_datetime < date_now:
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

                old_refresh.blacklist()

                res = Response(
                    {
                        "message": "New tokens updated."
                    },
                    status=status.HTTP_200_OK,
                )

                res.set_cookie(
                    key="access_token",
                    value=str(new_token.access_token),
                    httponly=True,
                    secure=True,
                    samesite="None",  # "Strict"
                    max_age=3600,  # 1 hora de expiração
                )
                res.set_cookie(
                    key="refresh_token",
                    value=new_token,
                    httponly=True,
                    secure=True,
                    samesite="None",  # "Strict"
                    max_age=3600 * 24,  # 1 dia de expiração
                )

                return res
            else:
                return Response({"message": "Token is valid.", "timestamp": {"token": exp_datetime, "now": date_now.strftime("%Y-%m-%dT%H:%M:%S")}}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            access_token = request.COOKIES.get("access_token")
            refresh_token = request.COOKIES.get("refresh_token")

            if not refresh_token:
                return Response(
                    {"detail": "token é obrigatório."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            getToken = JwtAccessToken.objects.filter(access_token=access_token)

            if getToken.first() == None:
                JwtAccessToken.objects.create(access_token=access_token).save()

            token_r = RefreshToken(refresh_token)

            token_r.check_blacklist()

            token_r.blacklist()

            response = Response(
                {"detail": "Logout realizado com sucesso."},
                status=status.HTTP_200_OK,
            )

            response.set_cookie(
                key="access_token",
                value="",
                httponly=True,
                secure=True,
                samesite="None",  # "Strict"
                max_age=1,
            )
            response.set_cookie(
                key="refresh_token",
                value="",
                httponly=True,
                secure=True,
                samesite="None",  # "Strict"
                max_age=1,
            )

            return response
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CheckAuthViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthenticationDefault]

    def list(self, request):
        return Response({"message": "Is Authenticated"}, status=status.HTTP_200_OK)
