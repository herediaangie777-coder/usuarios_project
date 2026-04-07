from rest_framework.routers import DefaultRouter

from api.config import EquipoViewSet, JuegoViewSet, PlataformaViewSet
from django.urls import path
from . import formulario_usuario

urlpatterns = [
    path('formulario/', formulario_usuario, name='formulario'),
]
router = DefaultRouter()
router.register(r"plataformas", PlataformaViewSet, basename="plataforma")
router.register(r"juegos", JuegoViewSet, basename="juego")
router.register(r"equipos", EquipoViewSet, basename="equipo")

urlpatterns = router.urls
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    
    path('', include('esports.urls')),  # 👈 ESTA ES LA CLAVE
]