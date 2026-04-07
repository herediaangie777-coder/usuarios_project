from django.urls import path
from .views import formulario_usuario

urlpatterns = [
    path('formulario/', formulario_usuario),
]