from rest_framework import serializers, viewsets

from artista.models import Artista
from .serializers import ArtistaSerializer

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class ArtistaViewSet(viewsets.ModelViewSet):
    serializer_class = ArtistaSerializer
    queryset = Artista.objects.all()


def create(self, request):
    serializer = ArtistaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
