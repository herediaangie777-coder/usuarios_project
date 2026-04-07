from django.core.exceptions import ValidationError
from django.db import models

from .equipo import EquipoJuego
from .juego import Juego
from .usuario import Arbitro, Atleta


class SesionEntrenamiento(models.Model):
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(max_length=20)
    puntos_experiencia = models.IntegerField(default=0)

    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    arbitro = models.ForeignKey(Arbitro, on_delete=models.CASCADE)

    atleta = models.ForeignKey(Atleta, on_delete=models.CASCADE, null=True, blank=True)
    equipo = models.ForeignKey(EquipoJuego, on_delete=models.CASCADE, null=True, blank=True)

    def iniciar_sesion(self):
        self.estado = "iniciada"
        self.save(update_fields=["estado"])

    def cancelar_sesion(self, motivo):
        if motivo:
            self.estado = "cancelada"
        else:
            self.estado = "cancelada"
        self.save(update_fields=["estado"])

    def cerrar_sesion(self):
        self.estado = "cerrada"
        self.save(update_fields=["estado"])

    def clean(self):
        if self.atleta and self.equipo:
            raise ValidationError("Solo puede haber atleta o equipo, no ambos.")
        if not self.atleta and not self.equipo:
            raise ValidationError("Debe asignar un atleta o un equipo.")
