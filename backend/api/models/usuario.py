import uuid
from django.db import models

# Función para generar un código automático si no llega uno
def generar_codigo_unico():
    return f"USR-{uuid.uuid4().hex[:6].upper()}"

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

    # Se permite nulo/blanco para evitar el IntegrityError en SQL Server
    codigo = models.CharField(
        max_length=50, 
        unique=True, 
        null=True, 
        blank=True, 
        default=generar_codigo_unico
    )
    tipo_documento = models.CharField(max_length=5, choices=TipoDocumento.choices)
    numero_documento = models.CharField(max_length=30, unique=True)
    nombre_completo = models.CharField(max_length=150)
    edad = models.PositiveSmallIntegerField()
    sexo = models.CharField(max_length=1, choices=Sexo.choices)
    direccion = models.CharField(max_length=200)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    tipo_usuario = models.CharField(max_length=50, blank=True, null=True)
    nivel = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def asignar_trofeo(self, trofeo):
        self.trofeos.add(trofeo)
        atleta = getattr(self, "atleta", None)
        if atleta:
            atleta.puntos_experiencia += trofeo.puntos
            atleta.nivel = max(1, (atleta.puntos_experiencia // 100) + 1)
            atleta.save(update_fields=["puntos_experiencia", "nivel"])
        return trofeo

    def __str__(self):
        return f"{self.nombre_completo} ({self.codigo})"

# Al heredar de Usuario, Django crea automáticamente el enlace. 
# NO agregues un campo 'usuario' manualmente aquí.
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


class AcudienteAtleta(models.Model):
    atleta = models.OneToOneField(
        "Atleta",
        on_delete=models.CASCADE,
        related_name="datos_acudiente",
    )
    nombre_completo = models.CharField(max_length=150)
    tipo_documento = models.CharField(max_length=5, choices=Usuario.TipoDocumento.choices)
    numero_documento = models.CharField(max_length=30)
    telefono = models.CharField(max_length=30)
    parentesco = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):
        return f"{self.nombre_completo} -> {self.atleta.nombre_completo}"

class Telefono(models.Model):
    # Uso de comillas para evitar errores de carga
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='telefonos')
    numero = models.CharField(max_length=30)
    tipo = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.numero} - {self.usuario.nombre_completo}"

class RedSocial(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name="redes")
    plataforma = models.CharField(max_length=50)
    usuario_red = models.CharField(max_length=100)

    def __str__(self):
        return self.plataforma
