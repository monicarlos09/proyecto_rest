from django.db import models


class Disquera(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    creado = models.DateTimeField(auto_now_add=True)
    editado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
