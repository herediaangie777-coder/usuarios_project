from django.contrib import admin
from django.urls import include, path
from rest_framework.schemas import get_schema_view

from esports import views

schema_view = get_schema_view(title="Centro de Entrenamiento E-Sports API")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("docs/", views.docs_page, name="docs_api"),
    path("docs/schema/", schema_view, name="docs_schema"),
    path("", views.inicio, name="inicio"),
    path("usuarios/", views.usuarios_lista, name="usuarios_lista"),
    path("usuarios/nuevo/", views.usuarios_formulario, name="usuarios_formulario"),
    path("usuarios/data/", views.usuarios_data, name="usuarios_data"),
    path("usuarios/crear/", views.crear_usuario, name="crear_usuario"),
    path("sesiones/", views.sesiones_lista, name="sesiones_lista"),
    path("sesiones/agendar/", views.entrenamientos_form, name="entrenamientos_form"),
    path("sesiones/crear/", views.crear_sesion, name="crear_sesion"),
    path("sesiones/<int:sesion_id>/iniciar/", views.iniciar_sesion, name="iniciar_sesion"),
    path("sesiones/<int:sesion_id>/cerrar/", views.cerrar_sesion, name="cerrar_sesion"),
    path("api/v1/", include("api.urls")),
]
