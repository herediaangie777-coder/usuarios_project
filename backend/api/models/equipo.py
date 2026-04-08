from django.db import models


class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    juego = models.CharField(max_length=100, blank=True, default="")
    horas_juego = models.CharField(max_length=50, blank=True, default="0")
    nivel = models.IntegerField(default=1)
    puntos_experiencia = models.PositiveIntegerField(default=0)
    usuarios = models.ManyToManyField("Atleta", related_name="equipos", blank=True)
    trofeos = models.ManyToManyField("Trofeo", related_name="equipos", blank=True)

    def asignar_atleta(self, usuario):
        self.usuarios.add(usuario)
        self.save()

    def calcular_nivel(self):
        puntos_trofeos_equipo = sum(trofeo.puntos for trofeo in self.trofeos.all())
        puntos_trofeos_atletas = sum(
            trofeo.puntos for atleta in self.usuarios.all() for trofeo in atleta.trofeos.all()
        )
        total = self.puntos_experiencia + puntos_trofeos_equipo + puntos_trofeos_atletas
        self.nivel = max(1, (total // 100) + 1)
        self.save(update_fields=["nivel"])
        return self.nivel

    def __str__(self):
        return self.nombre
