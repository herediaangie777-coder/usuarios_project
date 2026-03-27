from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UsuarioSerializer, TelefonoSerializer
from .services import UsuarioService, ServiceError


def api_response(status_name, data=None, message="", http_status=status.HTTP_200_OK):
    payload = {
        "status": status_name,
        "data": data if data is not None else {},
        "message": message,
    }
    return Response(payload, status=http_status)


class UsuarioListCreateView(APIView):
    def get(self, request):
        usuarios = UsuarioService.listar_usuarios()
        data = UsuarioSerializer(usuarios, many=True).data
        return api_response("success", data, "Listado de usuarios")

    def post(self, request):
        try:
            usuario = UsuarioService.crear_usuario(request.data)
        except ServiceError as exc:
            return api_response("error", exc.data, exc.message, status.HTTP_400_BAD_REQUEST)
        data = UsuarioSerializer(usuario).data
        return api_response("success", data, "Usuario creado", status.HTTP_201_CREATED)


class UsuarioDetailView(APIView):
    def get(self, request, usuario_id):
        try:
            usuario = UsuarioService.obtener_usuario(usuario_id)
        except Http404:
            return api_response("error", {}, "Usuario no encontrado", status.HTTP_404_NOT_FOUND)
        data = UsuarioSerializer(usuario).data
        return api_response("success", data, "Detalle de usuario")

    def put(self, request, usuario_id):
        try:
            usuario = UsuarioService.actualizar_usuario(usuario_id, request.data)
        except Http404:
            return api_response("error", {}, "Usuario no encontrado", status.HTTP_404_NOT_FOUND)
        except ServiceError as exc:
            return api_response("error", exc.data, exc.message, status.HTTP_400_BAD_REQUEST)
        data = UsuarioSerializer(usuario).data
        return api_response("success", data, "Usuario actualizado")

    def delete(self, request, usuario_id):
        try:
            UsuarioService.eliminar_usuario(usuario_id)
        except Http404:
            return api_response("error", {}, "Usuario no encontrado", status.HTTP_404_NOT_FOUND)
        return api_response("success", {}, "Usuario eliminado", status.HTTP_200_OK)


class TelefonoListCreateView(APIView):
    def get(self, request, usuario_id):
        try:
            telefonos = UsuarioService.listar_telefonos(usuario_id)
        except Http404:
            return api_response("error", {}, "Usuario no encontrado", status.HTTP_404_NOT_FOUND)
        data = TelefonoSerializer(telefonos, many=True).data
        return api_response("success", data, "Listado de telefonos")

    def post(self, request, usuario_id):
        try:
            telefono = UsuarioService.agregar_telefono(usuario_id, request.data)
        except Http404:
            return api_response("error", {}, "Usuario no encontrado", status.HTTP_404_NOT_FOUND)
        except ServiceError as exc:
            return api_response("error", exc.data, exc.message, status.HTTP_400_BAD_REQUEST)
        data = TelefonoSerializer(telefono).data
        return api_response("success", data, "Telefono agregado", status.HTTP_201_CREATED)


class TelefonoDeleteView(APIView):
    def delete(self, request, telefono_id):
        try:
            UsuarioService.eliminar_telefono(telefono_id)
        except Http404:
            return api_response("error", {}, "Telefono no encontrado", status.HTTP_404_NOT_FOUND)
        return api_response("success", {}, "Telefono eliminado", status.HTTP_200_OK)
