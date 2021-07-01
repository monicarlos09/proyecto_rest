from rest_framework import viewsets

from .models import Cancion, Autor, Album
from .serializers import CancionSerializer, AutorSerializer, AlbumSerializer

from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CancionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    serializer_class = CancionSerializer
    queryset = Cancion.objects.all()


class AutorViewSet(viewsets.ModelViewSet):
    serializer_class = AutorSerializer
    queryset = Autor.objects.all()


class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()
