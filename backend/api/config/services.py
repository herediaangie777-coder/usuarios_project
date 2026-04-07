from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.db.models import Max
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from ..models import (
    Usuario,
    Atleta,
    Arbitro,
    EquipoJuego,
    Juego,
    Plataforma,
    Trofeo,
    Consola,
    Control,
    SesionEntrenamiento,
    Telefono,
    RedSocial,
)
from .serializers_full import (
    UsuarioSerializer,
    TelefonoSerializer,
    RedSocialSerializer,
    EquipoJuegoSerializer,
    TrofeoSerializer,
    JuegoSerializer,
    SesionEntrenamientoSerializer,
    ConsolaSerializer,
    ControlSerializer,
)


class ServiceError(Exception):
    def __init__(self, message, data=None):
        super().__init__(message)
        self.message = message
        self.data = data or {}


def _validate_or_error(serializer):
    try:
        serializer.is_valid(raise_exception=True)
    except serializers.ValidationError as exc:
        raise ServiceError("Validacion fallida", exc.detail)


class UsuarioService:
    @staticmethod
    def _next_codigo():
        max_codigo = Usuario.objects.aggregate(max_codigo=Max("codigo"))["max_codigo"]
        return (max_codigo or 0) + 1

    @staticmethod
    @transaction.atomic
    def crear_usuario(data):
        serializer = UsuarioSerializer(data=data)
        _validate_or_error(serializer)

        validated = dict(serializer.validated_data)
        telefonos_data = validated.pop("telefonos", [])
        redes_data = validated.pop("redes", [])

        validated["codigo"] = UsuarioService._next_codigo()
        if "password" in validated:
            validated["password"] = make_password(validated["password"])

        usuario = Usuario.objects.create(**validated)

        if telefonos_data:
            Telefono.objects.bulk_create(
                [Telefono(usuario=usuario, **telefono) for telefono in telefonos_data]
            )
        if redes_data:
            RedSocial.objects.bulk_create(
                [RedSocial(usuario=usuario, **red) for red in redes_data]
            )

        return usuario

    @staticmethod
    @transaction.atomic
    def actualizar_usuario(usuario_id, data):
        usuario = get_object_or_404(Usuario, pk=usuario_id)
        serializer = UsuarioSerializer(usuario, data=data, partial=True)
        _validate_or_error(serializer)

        validated = dict(serializer.validated_data)
        validated.pop("telefonos", None)
        validated.pop("redes", None)

        password = validated.pop("password", None)
        if password:
            usuario.password = make_password(password)

        for attr, value in validated.items():
            setattr(usuario, attr, value)
        usuario.save()
        return usuario

    @staticmethod
    @transaction.atomic
    def eliminar_usuario(usuario_id):
        usuario = get_object_or_404(Usuario, pk=usuario_id)
        usuario.delete()

    @staticmethod
    @transaction.atomic
    def agregar_telefono(usuario_id, data):
        usuario = get_object_or_404(Usuario, pk=usuario_id)
        serializer = TelefonoSerializer(data=data)
        _validate_or_error(serializer)
        telefono = Telefono.objects.create(usuario=usuario, **serializer.validated_data)
        return telefono

    @staticmethod
    @transaction.atomic
    def agregar_red_social(usuario_id, data):
        usuario = get_object_or_404(Usuario, pk=usuario_id)
        serializer = RedSocialSerializer(data=data)
        _validate_or_error(serializer)
        red = RedSocial.objects.create(usuario=usuario, **serializer.validated_data)
        return red

class TelefonoService:

    @staticmethod
    def agregar_telefono(usuario_id, data):
        from ..models import Usuario, Telefono

        usuario = Usuario.objects.get(pk=usuario_id)
        return Telefono.objects.create(usuario=usuario, **data)

class EquipoService:
    @staticmethod
    @transaction.atomic
    def crear_equipo(data):
        serializer = EquipoJuegoSerializer(data=data)
        _validate_or_error(serializer)

        validated = dict(serializer.validated_data)
        usuarios = validated.pop("usuarios_ids", [])
        trofeos = validated.pop("trofeos_ids", [])

        equipo = EquipoJuego.objects.create(**validated)
        if usuarios:
            equipo.usuarios.add(*usuarios)
        if trofeos:
            equipo.trofeos.add(*trofeos)
        return equipo

    @staticmethod
    @transaction.atomic
    def agregar_atleta(equipo_id, atleta_id):
        equipo = get_object_or_404(EquipoJuego, pk=equipo_id)
        atleta = get_object_or_404(Atleta, pk=atleta_id)
        equipo.usuarios.add(atleta)
        return equipo

    @staticmethod
    @transaction.atomic
    def asignar_trofeo(equipo_id, trofeo_id):
        equipo = get_object_or_404(EquipoJuego, pk=equipo_id)
        trofeo = get_object_or_404(Trofeo, pk=trofeo_id)
        equipo.trofeos.add(trofeo)
        return equipo

    @staticmethod
    def calcular_nivel(equipo_id):
        equipo = get_object_or_404(EquipoJuego, pk=equipo_id)
        return equipo.calcular_nivel()


class TrofeoService:
    @staticmethod
    @transaction.atomic
    def crear_trofeo(data):
        serializer = TrofeoSerializer(data=data)
        _validate_or_error(serializer)

        validated = dict(serializer.validated_data)
        usuarios = validated.pop("usuarios_ids", [])
        equipos = validated.pop("equipos_ids", [])

        trofeo = Trofeo.objects.create(**validated)
        if usuarios:
            trofeo.usuarios.add(*usuarios)
        if equipos:
            trofeo.equipos.add(*equipos)
        return trofeo

    @staticmethod
    @transaction.atomic
    def asignar_a_usuario(usuario_id, trofeo_id):
        usuario = get_object_or_404(Usuario, pk=usuario_id)
        trofeo = get_object_or_404(Trofeo, pk=trofeo_id)
        trofeo.usuarios.add(usuario)
        return trofeo

    @staticmethod
    @transaction.atomic
    def asignar_a_equipo(equipo_id, trofeo_id):
        equipo = get_object_or_404(EquipoJuego, pk=equipo_id)
        trofeo = get_object_or_404(Trofeo, pk=trofeo_id)
        trofeo.equipos.add(equipo)
        return trofeo


class JuegoService:
    @staticmethod
    @transaction.atomic
    def crear_juego(data):
        serializer = JuegoSerializer(data=data)
        _validate_or_error(serializer)

        validated = dict(serializer.validated_data)
        plataformas = validated.pop("plataformas_ids", [])

        juego = Juego.objects.create(**validated)
        if plataformas:
            juego.plataformas.add(*plataformas)
        return juego

    @staticmethod
    def listar_juegos():
        return Juego.objects.prefetch_related("plataformas").all()

    @staticmethod
    def obtener_juego(juego_id):
        return get_object_or_404(Juego.objects.prefetch_related("plataformas"), pk=juego_id)

    @staticmethod
    @transaction.atomic
    def actualizar_juego(juego_id, data):
        juego = JuegoService.obtener_juego(juego_id)
        serializer = JuegoSerializer(juego, data=data, partial=True)
        _validate_or_error(serializer)

        validated = dict(serializer.validated_data)
        plataformas = validated.pop("plataformas_ids", None)

        for attr, value in validated.items():
            setattr(juego, attr, value)
        juego.save()

        if plataformas is not None:
            juego.plataformas.set(plataformas)

        return juego

    @staticmethod
    @transaction.atomic
    def eliminar_juego(juego_id):
        juego = JuegoService.obtener_juego(juego_id)
        juego.delete()


class SesionService:
    @staticmethod
    @transaction.atomic
    def agendar_sesion(data):
        serializer = SesionEntrenamientoSerializer(data=data)
        _validate_or_error(serializer)

        validated = dict(serializer.validated_data)
        if not validated.get("estado"):
            validated["estado"] = "agendada"

        sesion = SesionEntrenamiento.objects.create(**validated)
        return sesion

    @staticmethod
    @transaction.atomic
    def cancelar_sesion(sesion_id):
        sesion = get_object_or_404(SesionEntrenamiento, pk=sesion_id)
        sesion.estado = "cancelada"
        sesion.save(update_fields=["estado"])
        return sesion

    @staticmethod
    @transaction.atomic
    def cerrar_sesion(sesion_id):
        sesion = get_object_or_404(SesionEntrenamiento, pk=sesion_id)
        sesion.estado = "cerrada"
        sesion.save(update_fields=["estado"])
        return sesion

    @staticmethod
    def calcular_horas(sesion_id):
        sesion = get_object_or_404(SesionEntrenamiento, pk=sesion_id)
        inicio = datetime.combine(sesion.fecha, sesion.hora_inicio)
        fin = datetime.combine(sesion.fecha, sesion.hora_fin)
        if fin <= inicio:
            raise ServiceError(
                "Validacion fallida",
                {"hora_fin": "La hora_fin debe ser mayor que hora_inicio."},
            )
        delta = fin - inicio
        return round(delta.total_seconds() / 3600, 2)

    @staticmethod
    @transaction.atomic
    def asignar_experiencia(sesion_id):
        sesion = get_object_or_404(SesionEntrenamiento, pk=sesion_id)
        puntos = sesion.puntos_experiencia or 0
        if puntos <= 0:
            return 0

        if sesion.atleta:
            atleta = sesion.atleta
            atleta.puntos_experiencia += puntos
            atleta.save(update_fields=["puntos_experiencia"])
            return puntos

        if sesion.equipo:
            atletas = sesion.equipo.usuarios.all()
            for atleta in atletas:
                atleta.puntos_experiencia += puntos
                atleta.save(update_fields=["puntos_experiencia"])
            return puntos * atletas.count()

        raise ServiceError(
            "Validacion fallida",
            {"sesion": "La sesion no tiene atleta ni equipo asignado."},
        )


class HardwareService:
    @staticmethod
    @transaction.atomic
    def crear_consola(data):
        serializer = ConsolaSerializer(data=data)
        _validate_or_error(serializer)
        consola = Consola.objects.create(**serializer.validated_data)
        return consola

    @staticmethod
    @transaction.atomic
    def crear_control(data):
        serializer = ControlSerializer(data=data)
        _validate_or_error(serializer)
        control = Control.objects.create(**serializer.validated_data)
        return control
