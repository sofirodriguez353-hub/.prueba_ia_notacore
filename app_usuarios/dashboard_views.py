from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Usuario


class DashboardAdminView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard_admin.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.rol != Usuario.Rol.ADMIN:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class DashboardProfesorView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard_profesor.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.rol != Usuario.Rol.PROFESOR:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class DashboardEstudianteView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard_estudiante.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.rol != Usuario.Rol.ESTUDIANTE:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
