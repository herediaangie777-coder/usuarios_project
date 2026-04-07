from django.db import models


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

    def asignar_trofeo(self, trofeo):
        self.trofeos.add(trofeo)

    def __str__(self):
        return self.nombre_completo


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
