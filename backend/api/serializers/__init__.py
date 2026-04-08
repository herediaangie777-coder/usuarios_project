from .plataforma_serializer import PlataformaSerializer
from .juego_serializer import JuegoSerializer
from .equipo_serializer import EquipoSerializer
from .sesion_serializer import SesionEntrenamientoSerializer
from .usuario_serializer import UsuarioSerializer, TelefonoSerializer, AcudienteAtletaSerializer

__all__ = [
    "PlataformaSerializer",
    "JuegoSerializer",
    "EquipoSerializer",
    "SesionEntrenamientoSerializer",
    "UsuarioSerializer",
    "TelefonoSerializer",
    "AcudienteAtletaSerializer",
]
