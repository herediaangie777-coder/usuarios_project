import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from api.models import Arbitro, Atleta, Equipo, SesionEntrenamiento, Usuario
from api.serializers.sesion_serializer import SesionEntrenamientoSerializer
from api.serializers.usuario_serializer import UsuarioSerializer


def inicio(request):
    return render(request, "pages/index.html")


def docs_page(request):
    return render(request, "pages/docs_api.html")


def usuarios_lista(request):
    usuarios = Usuario.objects.prefetch_related("telefonos").order_by("-id")
    return render(request, "pages/usuarios_lista.html", {"usuarios": usuarios})


def usuarios_formulario(request):
    equipos = Equipo.objects.order_by("nombre")
    return render(request, "pages/usuarios_formulario.html", {"equipos": equipos})


def usuarios_data(request):
    usuarios = Usuario.objects.prefetch_related("telefonos").order_by("-id")
    serializer = UsuarioSerializer(usuarios, many=True)
    return JsonResponse(serializer.data, safe=False)


@require_POST
def crear_usuario(request):
    payload = json.loads(request.body)
    serializer = UsuarioSerializer(data=payload)
    if serializer.is_valid():
        usuario = serializer.save()
        return JsonResponse(UsuarioSerializer(usuario).data, status=201)
    return JsonResponse(serializer.errors, status=400)


def sesiones_lista(request):
    sesiones = SesionEntrenamiento.objects.select_related("arbitro", "atleta", "equipo").order_by(
        "-fecha", "-hora_inicio"
    )
    return render(request, "pages/sesiones_lista.html", {"sesiones": sesiones})


def entrenamientos_form(request):
    context = {
        "usuarios": Atleta.objects.order_by("nombre_completo"),
        "arbitros": Arbitro.objects.order_by("nombre_completo"),
        "equipos": Equipo.objects.order_by("nombre"),
    }
    return render(request, "pages/entrenamientos_form.html", context)


@require_POST
def crear_sesion(request):
    payload = json.loads(request.body)
    serializer = SesionEntrenamientoSerializer(data=payload)
    if serializer.is_valid():
        sesion = serializer.save()
        return JsonResponse(SesionEntrenamientoSerializer(sesion).data, status=201)
    return JsonResponse(serializer.errors, status=400)


@require_POST
def iniciar_sesion(request, sesion_id):
    sesion = get_object_or_404(SesionEntrenamiento, pk=sesion_id)
    sesion.iniciar_sesion()
    return JsonResponse(SesionEntrenamientoSerializer(sesion).data)


@require_POST
def cerrar_sesion(request, sesion_id):
    sesion = get_object_or_404(SesionEntrenamiento, pk=sesion_id)
    puntos, trofeo = sesion.cerrar_sesion()
    data = SesionEntrenamientoSerializer(sesion).data
    data["recompensa"] = {
        "puntos_experiencia": puntos,
        "trofeo": trofeo.nombre,
    }
    return JsonResponse(data)
