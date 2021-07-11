from artista.models import Artista
from disquera.models import Disquera
from django.contrib.auth.models import User
from django.db import models


class Autor(models.Model):
    nombre = models.CharField(max_length=200)
    nacionalidad = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]


class Album(models.Model):
    nombre = models.CharField(max_length=100)
    anio_lanzamiento = models.DateField()

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]


class Cancion(models.Model):
    nombre = models.CharField(max_length=20)
    anio_lanzamiento = models.DateField()
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    creado = models.DateTimeField(auto_now_add=True)
    editado = models.DateTimeField(auto_now=True)

    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True)
    album = models.ManyToManyField(Album)
    artista = models.ManyToManyField(Artista)
    disquera = models.ManyToManyField(Disquera)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
