from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import SesionEntrenamiento
from api.serializers import SesionEntrenamientoSerializer


class SesionEntrenamientoViewSet(viewsets.ModelViewSet):
    queryset = SesionEntrenamiento.objects.select_related("arbitro", "atleta", "equipo").order_by(
        "-fecha", "-hora_inicio"
    )
    serializer_class = SesionEntrenamientoSerializer

    @action(detail=True, methods=["post"])
    def iniciar(self, request, pk=None):
        sesion = self.get_object()
        sesion.iniciar_sesion()
        serializer = self.get_serializer(sesion)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def cerrar(self, request, pk=None):
        sesion = self.get_object()
        puntos, trofeo = sesion.cerrar_sesion()
        serializer = self.get_serializer(sesion)
        payload = serializer.data
        payload["recompensa"] = {
            "puntos_experiencia": puntos,
            "trofeo": trofeo.nombre,
        }
        return Response(payload, status=status.HTTP_200_OK)
