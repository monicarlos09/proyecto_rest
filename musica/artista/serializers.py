from rest_framework import serializers

from artista.models import Artista, Disquera

from disquera.serializers import DisqueraSerializer


class ArtistaSerializer(serializers.ModelSerializer):
    disquera = DisqueraSerializer(many=True, read_only=True)

    disquera_entrada = serializers.PrimaryKeyRelatedField(
        queryset=Disquera.objects.all(), many=True, write_only=True)

    class Meta:
        model = Artista
        fields = '__all__'

    def create(self, validated_data):
        disquera_entrada = validated_data.pop('disquera_entrada')

        artista = Artista.objects.create(**validated_data)

        for disquera_entrada in disquera_entrada:
            artista.disquera.add(disquera_entrada)

        return artista

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.nacionalidad = validated_data.get(
            'nacionalidad', instance.nacionalidad)
        instance.fecha_nacimiento = validated_data.get(
            'fecha_nacimiento', instance.fecha_nacimiento)
        instance.genero = validated_data.get('genero', instance.genero)

        instance.disquera.set(validated_data.get(
            'disquera_entrada', instance.disquera.all()))

        instance.save()
        return instance
