from django.contrib import admin

from ..models import (
    Usuario,
    Atleta,
    Arbitro,
    Administrativo,
    Proveedor,
    AcudienteMinor,
    Telefono,
    RedSocial,
    Plataforma,
    Juego,
    Trofeo,
    EquipoJuego,
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
        Telefono,
        RedSocial,
        Plataforma,
        Juego,
        Trofeo,
        EquipoJuego,
        Consola,
        Control,
        SesionEntrenamiento,
    ]
)
