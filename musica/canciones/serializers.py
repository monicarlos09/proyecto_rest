import re
from rest_framework import serializers
from canciones.models import Cancion, Autor, Album

from artista.serializers import ArtistaSerializer
from disquera.serializers import DisqueraSerializer


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'


class CancionSerializer(serializers.ModelSerializer):
    album = AlbumSerializer(many=True, read_only=True)
    artista = ArtistaSerializer(many=True, read_only=True)
    disquera = DisqueraSerializer(many=True, read_only=True)

    nombre_autor = serializers.CharField(source='autor.nombre', read_only=True)

    class Meta:
        model = Cancion
        fields = '__all__'
        extra_kwargs = {'autor': {'write_only': True}}

    def create(self, validated_data):
        return Album.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.album = validated_data.get('album', instance.album)
        instance.artista = validated_data.get('artista', instance.artista)
        instance.disquera = validated_data.get('disquera', instance.disquera)
        instance.save()
        return instance
