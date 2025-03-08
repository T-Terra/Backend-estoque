from ..serializers.serializer import PecaSerializer
from ..models.peca import Peca
from rest_framework import viewsets


"""Rotas da api"""


class PecaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Peca.objects.all()
    serializer_class = PecaSerializer
