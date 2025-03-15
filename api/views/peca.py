from api.auth.auth_custom import JWTAuthenticationDefault
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from ..serializers.serializer import PecaSerializer
from ..models.peca import Peca
from ..auth.permissions import ApiAccessPermission


"""ViewSet que cria todas as actions da api CRUD"""


class PecaViewSet(viewsets.ModelViewSet):
    queryset = Peca.objects.all()
    serializer_class = PecaSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthenticationDefault]

    def destroy(self, request, pk):
        get_object_or_404(Peca, pk=pk).delete()
        return Response(
            {"message": "produto deletado com sucesso.", "id": pk},
            status=status.HTTP_200_OK,
        )
