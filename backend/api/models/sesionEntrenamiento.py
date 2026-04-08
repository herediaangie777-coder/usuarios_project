from django.db import models
from django.utils import timezone


class SesionEntrenamiento(models.Model):
    ESTADOS = [
        ("programada", "Programada"),
        ("en curso", "En Curso"),
        ("cerrada", "Cerrada"),
        ("cancelada", "Cancelada"),
    ]

    juego = models.CharField(max_length=100, default="Valorant")
    fecha = models.DateField(default=timezone.now)
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)
    arbitro = models.ForeignKey(
        "Arbitro",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sesiones_supervisadas",
    )
    atleta = models.ForeignKey(
        "Atleta",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sesiones_entrenamiento",
    )
    equipo = models.ForeignKey(
        "Equipo",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sesiones_entrenamiento",
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default="programada")
    puntos_experiencia = models.PositiveIntegerField(default=0)
    hora_inicio_real = models.DateTimeField(null=True, blank=True)
    motivo_cancelacion = models.TextField(null=True, blank=True)

    def iniciar_sesion(self):
        self.estado = "en curso"
        self.hora_inicio_real = timezone.now()
        self.save(update_fields=["estado", "hora_inicio_real"])

    @property
    def duracion_minutos(self):
        if not self.hora_inicio or not self.hora_fin:
            return 0
        inicio = timezone.datetime.combine(self.fecha, self.hora_inicio)
        fin = timezone.datetime.combine(self.fecha, self.hora_fin)
        if fin <= inicio:
            return 0
        return int((fin - inicio).total_seconds() // 60)

    def calcular_recompensa(self):
        minutos = self.duracion_minutos
        base = 25
        if minutos >= 120:
            base = 120
        elif minutos >= 90:
            base = 90
        elif minutos >= 60:
            base = 60
        elif minutos >= 30:
            base = 40

        if self.equipo_id:
            base += 20

        return base

    def cancelar_sesion(self, motivo="Cancelado por el usuario"):
        self.estado = "cancelada"
        self.motivo_cancelacion = motivo
        self.save(update_fields=["estado", "motivo_cancelacion"])

    def cerrar_sesion(self):
        recompensa = self.calcular_recompensa()
        self.estado = "cerrada"
        self.puntos_experiencia = recompensa
        self.save(update_fields=["estado", "puntos_experiencia"])

        nombre_trofeo, descripcion = self._definir_trofeo(recompensa)
        trofeo, _ = self._meta.apps.get_model("api", "Trofeo").objects.get_or_create(
            nombre=nombre_trofeo,
            juego=self.juego,
            defaults={
                "puntos": recompensa,
                "descripcion": descripcion,
            },
        )

        if self.atleta_id:
            self.atleta.puntos_experiencia += recompensa
            self.atleta.nivel = max(1, (self.atleta.puntos_experiencia // 100) + 1)
            self.atleta.save()
            trofeo.usuarios.add(self.atleta)

        if self.equipo_id:
            self.equipo.puntos_experiencia += recompensa
            self.equipo.nivel = max(1, (self.equipo.puntos_experiencia // 100) + 1)
            self.equipo.save()
            trofeo.equipos.add(self.equipo)
            for atleta in self.equipo.usuarios.all():
                atleta.puntos_experiencia += recompensa // 2
                atleta.nivel = max(1, (atleta.puntos_experiencia // 100) + 1)
                atleta.save()
                trofeo.usuarios.add(atleta)

        return recompensa, trofeo

    def _definir_trofeo(self, recompensa):
        if recompensa >= 120:
            return "Leyenda del Scrim", "Sesiones largas con rendimiento competitivo."
        if recompensa >= 90:
            return "Dominio Tactico", "Entrenamiento avanzado con alta intensidad."
        if recompensa >= 60:
            return "Rutina Consistente", "Sesion completa con buen tiempo de practica."
        return "Primer Paso", "Sesion corta completada con exito."

    def __str__(self):
        return f"{self.juego} - {self.fecha}"
