from rest_framework.viewsets import ModelViewSet

from api.models import Plataforma
from api.serializers import PlataformaSerializer


class PlataformaViewSet(ModelViewSet):
    queryset = Plataforma.objects.all()
    serializer_class = PlataformaSerializer
