from artista.models import Artista
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import ArtistaSerializer


class ArtistaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    serializer_class = ArtistaSerializer
    queryset = Artista.objects.all()
