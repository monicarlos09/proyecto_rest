from rest_framework import serializers, viewsets

from artista.models import Artista
from .serializers import ArtistaSerializer


class ArtistaViewSet(viewsets.ModelViewSet):
    serializer_class = ArtistaSerializer
    queryset = Artista.objects.all()
