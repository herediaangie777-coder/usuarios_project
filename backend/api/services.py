from django.shortcuts import get_object_or_404

from api.models import Atleta, Equipo, SesionEntrenamiento


class UsuarioService:
    @staticmethod
    def listar():
        return Atleta.objects.prefetch_related("telefonos").order_by("-id")

    @staticmethod
    def obtener(usuario_id):
        return get_object_or_404(Atleta, pk=usuario_id)


class EquipoService:
    @staticmethod
    def listar():
        return Equipo.objects.prefetch_related("usuarios", "trofeos").order_by("nombre")

    @staticmethod
    def recalcular_nivel(equipo_id):
        equipo = get_object_or_404(Equipo, pk=equipo_id)
        equipo.calcular_nivel()
        return equipo


class SesionService:
    @staticmethod
    def listar():
        return SesionEntrenamiento.objects.select_related("atleta", "equipo").order_by(
            "-fecha", "-hora_inicio"
        )

    @staticmethod
    def iniciar(sesion_id):
        sesion = get_object_or_404(SesionEntrenamiento, pk=sesion_id)
        sesion.iniciar_sesion()
        return sesion

    @staticmethod
    def cerrar(sesion_id):
        sesion = get_object_or_404(SesionEntrenamiento, pk=sesion_id)
        sesion.cerrar_sesion()
        return sesion
