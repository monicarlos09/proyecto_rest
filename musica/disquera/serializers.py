from rest_framework import serializers
from .models import Disquera


class DisqueraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disquera
        fields = '__all__'
