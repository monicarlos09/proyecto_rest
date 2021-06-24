from django.shortcuts import render
from rest_framework import serializers, viewsets
from .models import Artista
from .serializers import ArtistaSerializer


class ArtistaViewSet(viewsets.ModelViewSet):
    serializer_class = ArtistaSerializer
    queryset = Artista.objects.all()
