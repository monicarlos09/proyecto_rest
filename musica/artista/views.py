from rest_framework import serializers, viewsets

from artista.models import Artista
from .serializers import ArtistaSerializer

from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ArtistaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    serializer_class = ArtistaSerializer
    queryset = Artista.objects.all()
