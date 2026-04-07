from django.db import models

from .plataforma import Plataforma


class Juego(models.Model):
    nombre = models.CharField(max_length=100)
    clasificacion_esrb = models.CharField(max_length=10)
    desarrollador = models.CharField(max_length=100)
    numero_jugadores = models.IntegerField()
    tipo = models.CharField(max_length=20)
    existencias = models.IntegerField()

    plataformas = models.ManyToManyField(Plataforma, related_name="juegos")

    def registrar_existencia(self, cantidad):
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self.existencias += cantidad
        self.save(update_fields=["existencias"])

    def __str__(self):
        return self.nombre
