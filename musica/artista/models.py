from disquera.models import Disquera
from django.db import models


class Artista(models.Model):
    nombre = models.CharField(max_length=200)
    nacionalidad = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    disquera = models.ManyToManyField(Disquera)
    creado = models.DateTimeField(auto_now_add=True)
    editado = models.DateTimeField(auto_now=True)

    lista_genero = (
        ("POP", "POP"),
        ("ROCK", "ROCK"),
        ("RANCHERO", "RANCHERO"),
    )

    genero = models.CharField(
        max_length=8,
        choices=lista_genero,
        blank=True,
        null=True,
        default="POP",
        help_text="Genero del artisita",
    )

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
