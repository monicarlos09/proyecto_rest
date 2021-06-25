from rest_framework import serializers
from artista.models import Artista

from disquera.serializers import DisqueraSerializer


class ArtistaSerializer(serializers.ModelSerializer):
    disquera = DisqueraSerializer(many=True, read_only=True)

    class Meta:
        model = Artista
        fields = '__all__'

    def create(self, validated_data):
        return Artista.objects.create(validated_data)
