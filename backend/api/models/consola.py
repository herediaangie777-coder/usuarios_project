from django.db import models

from .plataforma import Plataforma


class Hardware(models.Model):
    numero_serie = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Consola(Hardware):
    nombre = models.CharField(max_length=100)
    total_existentes = models.IntegerField()
    ip = models.GenericIPAddressField()
    mac_lan = models.CharField(max_length=50)
    mac_wifi = models.CharField(max_length=50)
    total_controles = models.IntegerField()

    plataforma = models.ForeignKey(Plataforma, on_delete=models.CASCADE)

    def registrar_entrada(self):
        self.total_existentes += 1
        self.save(update_fields=["total_existentes"])

    def registrar_salida(self):
        if self.total_existentes <= 0:
            raise ValueError("No hay consolas disponibles para registrar salida.")
        self.total_existentes -= 1
        self.save(update_fields=["total_existentes"])
