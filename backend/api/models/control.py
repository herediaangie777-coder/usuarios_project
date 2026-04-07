from django.db import models

from .consola import Hardware
from .plataforma import Plataforma


class Control(Hardware):
    tipo = models.CharField(max_length=50)
    plataforma = models.ForeignKey(Plataforma, on_delete=models.CASCADE)
