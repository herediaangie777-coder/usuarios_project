from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import EquipoViewSet, JuegoViewSet, PlataformaViewSet

router = DefaultRouter()
router.register(r"plataformas", PlataformaViewSet, basename="plataforma")
router.register(r"juegos", JuegoViewSet, basename="juego")
router.register(r"equipos", EquipoViewSet, basename="equipo")

urlpatterns = [
    path("", include(router.urls)),
]
