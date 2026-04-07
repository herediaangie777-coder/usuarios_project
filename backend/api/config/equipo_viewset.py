from rest_framework.viewsets import ModelViewSet

from api.models import EquipoJuego
from api.serializers import EquipoSerializer


class EquipoViewSet(ModelViewSet):
    queryset = EquipoJuego.objects.all()
    serializer_class = EquipoSerializer
