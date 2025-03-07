from django.http import JsonResponse
from ..serializers.serializer import PecaSerializer
from ..models.peca import Peca


"""Rotas da api"""


def PecaAdd(req):
    if req.method == 'GET':
        queryDB = Peca.objects.all()
        serializer = PecaSerializer(queryDB, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif req.method == 'POST':
        pass
