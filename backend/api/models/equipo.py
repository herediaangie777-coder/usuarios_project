from django.db import models

from .juego import Juego
from .usuario import Atleta
from .trofeo import Trofeo


class EquipoJuego(models.Model):
    nombre = models.CharField(max_length=100)
    horas_juego = models.IntegerField(default=0)

    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    usuarios = models.ManyToManyField(Atleta, related_name="equipos")

    trofeos = models.ManyToManyField(Trofeo, related_name="equipos", blank=True)

    def calcular_nivel(self):
        return sum(t.puntos for t in self.trofeos.all())

    def asignar_atleta(self, usuario):
        if not isinstance(usuario, Atleta):
            raise ValueError("Solo se pueden asignar usuarios tipo Atleta.")
        self.usuarios.add(usuario)

    def __str__(self):
        return self.nombre
