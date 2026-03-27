from django.db import models
from django.core.exceptions import ValidationError


# =========================
# USUARIO
# =========================
class Usuario(models.Model):
    class TipoDocumento(models.TextChoices):
        CC = "CC", "Cedula"
        CE = "CE", "Cedula extranjeria"
        TI = "TI", "Tarjeta identidad"
        PAS = "PAS", "Pasaporte"

    class Sexo(models.TextChoices):
        M = "M", "Masculino"
        F = "F", "Femenino"
        O = "O", "Otro"

    codigo = models.PositiveIntegerField(unique=True)
    tipo_documento = models.CharField(max_length=5, choices=TipoDocumento.choices)
    numero_documento = models.CharField(max_length=30, unique=True)
    nombre_completo = models.CharField(max_length=150)
    edad = models.PositiveSmallIntegerField()
    sexo = models.CharField(max_length=1, choices=Sexo.choices)
    direccion = models.CharField(max_length=200)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    tipo_usuario = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_completo


# =========================
# HERENCIAS
# =========================
class Atleta(Usuario):
    puntos_experiencia = models.IntegerField(default=0)


class Arbitro(Usuario):
    pass


class Administrativo(Usuario):
    pass


class Proveedor(Usuario):
    pass


class AcudienteMinor(Usuario):
    pass


# =========================
# CONTACTO
# =========================
class Telefono(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="telefonos")
    numero = models.CharField(max_length=30)
    tipo = models.CharField(max_length=10)

    def __str__(self):
        return self.numero


class RedSocial(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="redes")
    plataforma = models.CharField(max_length=50)
    usuario_red = models.CharField(max_length=100)

    def __str__(self):
        return self.plataforma


# =========================
# JUEGOS
# =========================
class Plataforma(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Juego(models.Model):
    nombre = models.CharField(max_length=100)
    clasificacion_esrb = models.CharField(max_length=10)
    desarrollador = models.CharField(max_length=100)
    numero_jugadores = models.IntegerField()
    tipo = models.CharField(max_length=20)
    existencias = models.IntegerField()

    plataformas = models.ManyToManyField(Plataforma, related_name="juegos")

    def __str__(self):
        return self.nombre


# =========================
# TROFEOS
# =========================
class Trofeo(models.Model):
    nombre = models.CharField(max_length=100)
    puntos = models.IntegerField()
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)

    usuarios = models.ManyToManyField(Usuario, related_name="trofeos", blank=True)

    def __str__(self):
        return self.nombre


# =========================
# EQUIPOS
# =========================
class EquipoJuego(models.Model):
    nombre = models.CharField(max_length=100)
    horas_juego = models.IntegerField(default=0)

    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    usuarios = models.ManyToManyField(Atleta, related_name="equipos")

    trofeos = models.ManyToManyField(Trofeo, related_name="equipos", blank=True)

    def calcular_nivel(self):
        return sum(t.puntos for t in self.trofeos.all())

    def __str__(self):
        return self.nombre


# =========================
# HARDWARE
# =========================
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


class Control(Hardware):
    tipo = models.CharField(max_length=50)
    plataforma = models.ForeignKey(Plataforma, on_delete=models.CASCADE)


# =========================
# SESIONES
# =========================
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

    def clean(self):
        if self.atleta and self.equipo:
            raise ValidationError("Solo puede haber atleta o equipo, no ambos.")
        if not self.atleta and not self.equipo:
            raise ValidationError("Debe asignar un atleta o un equipo.")