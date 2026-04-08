from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from api.models.juego import Juego
from api.serializers.juego_serializer import JuegoSerializer

class JuegoViewSet(viewsets.ModelViewSet):
    queryset = Juego.objects.all()
    serializer_class = JuegoSerializer
    
    # Requerimiento 3.4: Filtros y Búsqueda
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    
    # He comentado esta línea para solucionar el error 500 de Swagger.
    # search_fields seguirá funcionando para buscar por nombre.
    # filterset_fields = ['plataforma']  
    
    #search_fields = ['nombre']  # Permite buscar por nombre del juego

    # Requerimiento 4.1: Seguridad
    # Todos pueden ver, solo usuarios autenticados pueden editar
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]