from disquera.models import Disquera
from artista.models import Artista
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

    album_entrada = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(), many=True, write_only=True)

    artista_entrada = serializers.PrimaryKeyRelatedField(
        queryset=Artista.objects.all(), many=True, write_only=True)

    disquera_entrada = serializers.PrimaryKeyRelatedField(
        queryset=Disquera.objects.all(), many=True, write_only=True)

    nombre_autor = serializers.CharField(source='autor.nombre', read_only=True)

    class Meta:
        model = Cancion
        fields = '__all__'
        extra_kwargs = {'autor': {'write_only': True}}

    def create(self, validated_data):
        album_data = validated_data.pop('album_entrada')
        artista_entrada = validated_data.pop('artista_entrada')
        disquera_entrada = validated_data.pop('disquera_entrada')

        cancion = Cancion.objects.create(**validated_data)

        for album_data in album_data:
            cancion.album.add(album_data)

        for artista_entrada in artista_entrada:
            cancion.artista.add(artista_entrada)

        for disquera_entrada in disquera_entrada:
            cancion.disquera.add(disquera_entrada)

        return cancion

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.anio_lanzamiento = validated_data.get(
            'anio_lanzamiento', instance.anio_lanzamiento)
        instance.precio = validated_data.get('precio', instance.precio)
        instance.autor = validated_data.get('autor', instance.autor)

        instance.album.set(validated_data.get(
            'album_entrada', instance.album.all()))
        instance.artista.set(validated_data.get(
            'artista_entrada', instance.artista.all()))
        instance.disquera.set(validated_data.get(
            'disquera_entrada', instance.disquera.all()))

        instance.save()
        return instance
