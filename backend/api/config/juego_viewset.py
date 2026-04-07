from rest_framework.viewsets import ModelViewSet

from api.models import Juego
from api.serializers import JuegoSerializer


class JuegoViewSet(ModelViewSet):
    queryset = Juego.objects.all()
    serializer_class = JuegoSerializer
