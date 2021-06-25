from rest_framework import viewsets

from .models import Disquera
from .serializers import DisqueraSerializer


class DisqueraViewSet(viewsets.ModelViewSet):
    serializer_class = DisqueraSerializer
    queryset = Disquera.objects.all()
