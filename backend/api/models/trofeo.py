from django.db import models


class Trofeo(models.Model):
    nombre = models.CharField(max_length=100)
    puntos = models.IntegerField()
    juego = models.CharField(max_length=100, blank=True, default="General")
    descripcion = models.CharField(max_length=255, blank=True, default="")
    usuarios = models.ManyToManyField("Usuario", related_name="trofeos", blank=True)

    def __str__(self):
        return self.nombre
