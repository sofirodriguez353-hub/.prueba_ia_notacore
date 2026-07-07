from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        return self.request.user.is_authenticated and self.request.user.rol == "ADMIN"

    def handle_no_permission(self) -> HttpResponseForbidden:
        return render(self.request, "errors/403.html", status=403)


class ProfesorRequiredMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        return self.request.user.is_authenticated and self.request.user.rol == "PROFESOR"

    def handle_no_permission(self) -> HttpResponseForbidden:
        return render(self.request, "errors/403.html", status=403)


class EstudianteRequiredMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        return self.request.user.is_authenticated and self.request.user.rol == "ESTUDIANTE"

    def handle_no_permission(self) -> HttpResponseForbidden:
        return render(self.request, "errors/403.html", status=403)
