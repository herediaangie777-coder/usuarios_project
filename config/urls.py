from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.usuarios.urls")),
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    re_path(r"^frontend/(?P<path>.*)$", serve, {"document_root": settings.BASE_DIR / "frontend"}),
]
