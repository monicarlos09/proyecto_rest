from rest_framework import serializers
from .models import Cancion, Autor, Album


class CancionSerializer(serializers.ModelSerializer):
    nombre_autor = serializers.CharField(source='autor.nombre', read_only=True)

    class Meta:
        model = Cancion
        fields = '__all__'
        extra_kwargs = {'autor': {'write_only': True}}


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'
