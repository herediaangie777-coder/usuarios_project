from rest_framework import viewsets

from api.models import Usuario
from api.serializers import UsuarioSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.prefetch_related("telefonos").order_by("-id")
    serializer_class = UsuarioSerializer
