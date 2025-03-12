from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from ..models.jwt_access_token import JwtAccessToken

"""Classe de Autenticação JWT personalizada"""


class JWTAuthenticationDefault(JWTAuthentication):
    def authenticate(self, request):
        # Tenta pegar o token no cookie 'access_token'
        token = request.COOKIES.get("access_token")

        get_token = JwtAccessToken.objects.filter(access_token=token)

        if not token:
            raise AuthenticationFailed("Authentication credentials were not provided.")

        if get_token.first() != None:
            raise AuthenticationFailed("Token expired.")

        try:
            # Valida o token
            validated_token = self.get_validated_token(token)
        except Exception as e:
            raise AuthenticationFailed(f"Invalid token: {e}")

        # Retorna o usuário e o token validado
        return self.get_user(validated_token), validated_token
