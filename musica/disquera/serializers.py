from disquera.models import Disquera
from rest_framework import serializers


class DisqueraSerializer(serializers.ModelSerializer):
    usuario = serializers.CharField(source="usuario.username")

    class Meta:
        model = Disquera
        fields = "__all__"
