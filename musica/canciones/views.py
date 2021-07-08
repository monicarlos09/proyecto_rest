from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Album
from .models import Autor
from .models import Cancion
from .serializers import AlbumSerializer
from .serializers import AutorSerializer
from .serializers import CancionSerializer


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
