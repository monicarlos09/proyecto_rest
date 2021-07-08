from rest_framework import viewsets

from .models import Disquera
from .permissions import IsAuthorOrReadOnly
from .serializers import DisqueraSerializer


class DisqueraViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)

    serializer_class = DisqueraSerializer
    queryset = Disquera.objects.all()

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def perform_update(self, serializer):
        serializer.save(usuario=self.request.user)
