from django.urls import path

from .views import (
    UsuarioListCreateView,
    UsuarioDetailView,
    TelefonoListCreateView,
    TelefonoDeleteView,
)

urlpatterns = [
    path("usuarios/", UsuarioListCreateView.as_view(), name="usuarios-list"),
    path("usuarios/<int:usuario_id>/", UsuarioDetailView.as_view(), name="usuarios-detail"),
    path(
        "usuarios/<int:usuario_id>/telefonos/",
        TelefonoListCreateView.as_view(),
        name="telefonos-list",
    ),
    path("telefonos/<int:telefono_id>/", TelefonoDeleteView.as_view(), name="telefonos-delete"),
]
