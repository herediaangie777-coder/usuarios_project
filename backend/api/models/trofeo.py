from django.db import models

from .juego import Juego
from .usuario import Usuario


class Trofeo(models.Model):
    nombre = models.CharField(max_length=100)
    puntos = models.IntegerField()
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)

    usuarios = models.ManyToManyField(Usuario, related_name="trofeos", blank=True)

    def __str__(self):
        return self.nombre
