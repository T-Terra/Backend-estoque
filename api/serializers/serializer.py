from rest_framework import serializers
from api.models.peca import Peca


class PecaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peca
        fields = "__all__"
