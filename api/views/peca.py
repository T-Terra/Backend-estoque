from api.auth.auth_custom import JWTAuthenticationDefault
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


from ..serializers.serializer import PecaSerializer
from ..models.peca import Peca
from ..auth.permissions import ApiAccessPermission


"""ViewSet que cria todas as actions da api CRUD"""


class PecaViewSet(viewsets.ModelViewSet):
    queryset = Peca.objects.all()
    serializer_class = PecaSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthenticationDefault]
