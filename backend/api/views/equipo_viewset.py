from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Equipo
from api.serializers import EquipoSerializer


class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all().order_by("nombre")
    serializer_class = EquipoSerializer

    @action(detail=True, methods=["post"])
    def recalcular(self, request, pk=None):
        equipo = self.get_object()
        nivel = equipo.calcular_nivel()
        return Response({"id": equipo.id, "nivel": nivel})
