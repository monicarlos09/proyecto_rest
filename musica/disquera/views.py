from rest_framework import viewsets

from .models import Disquera
from .serializers import DisqueraSerializer

from rest_framework.permissions import IsAuthenticatedOrReadOnly


class DisqueraViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    serializer_class = DisqueraSerializer
    queryset = Disquera.objects.all()
