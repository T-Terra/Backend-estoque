from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

"""Classe de Autenticação JWT personalizada"""


class JWTAuthenticationDefault(JWTAuthentication):
    def authenticate(self, request):
        # Tenta pegar o token no cookie 'access_token'
        token = request.COOKIES.get("access_token")

        if not token:
            raise AuthenticationFailed("Authentication credentials were not provided.")

        try:
            # Valida o token
            validated_token = self.get_validated_token(token)
        except Exception as e:
            raise AuthenticationFailed(f"Invalid token: {e}")

        # Retorna o usuário e o token validado
        return self.get_user(validated_token), validated_token
