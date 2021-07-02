from django.db import models
from django.contrib.auth.models import User


class Disquera(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    creado = models.DateTimeField(auto_now_add=True)
    editado = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        #cadena = self.nombre+","+self.direccion+","+self.telefono
        # return cadena
        return self.nombre

    class Meta:
        ordering = ['nombre']
