from django.contrib import admin
from django.urls import include, path

from app_usuarios.dashboard_views import DashboardAdminView, DashboardEstudianteView, DashboardProfesorView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("usuarios/", include(("app_usuarios.urls", "usuarios"), namespace="usuarios")),
    path("academico/", include(("app_academico.urls", "academico"), namespace="academico")),
    path("dashboard/admin/", DashboardAdminView.as_view(), name="dashboard_admin"),
    path("dashboard/profesor/", DashboardProfesorView.as_view(), name="dashboard_profesor"),
    path("dashboard/estudiante/", DashboardEstudianteView.as_view(), name="dashboard_estudiante"),
]
