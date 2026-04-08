from django.contrib import admin

from .models import (
    Usuario,
    Atleta,
    Arbitro,
    Administrativo,
    Proveedor,
    AcudienteMinor,
    AcudienteAtleta,
    Telefono,
    RedSocial,
    Plataforma,
    Juego,
    Trofeo,
    Equipo,
    Consola,
    Control,
    SesionEntrenamiento,
)

admin.site.register(
    [
        Usuario,
        Atleta,
        Arbitro,
        Administrativo,
        Proveedor,
        AcudienteMinor,
        AcudienteAtleta,
        Telefono,
        RedSocial,
        Plataforma,
        Juego,
        Trofeo,
        Equipo,
        Consola,
        Control,
        SesionEntrenamiento,
    ]
)
