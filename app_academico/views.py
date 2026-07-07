from typing import Any

from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from app_usuarios.permisos import AdminRequiredMixin
from app_usuarios.models import Usuario

from .forms import AulaVirtualForm, UsuarioSearchForm
from .models import AulaVirtual, Profesor


class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = "admin/dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["aulas_por_año"] = (
            AulaVirtual.objects.values("año_curso").annotate(total=Count("id")).order_by("año_curso")
        )
        context["total_profesores"] = Profesor.objects.count()
        context["total_estudiantes"] = Usuario.objects.filter(rol="ESTUDIANTE").count()
        context["total_aulas"] = AulaVirtual.objects.count()
        return context


class AulaListView(AdminRequiredMixin, ListView):
    model = AulaVirtual
    template_name = "admin/aula_list.html"
    context_object_name = "aulas"
    paginate_by = 10

    def get_queryset(self) -> Any:
        queryset = AulaVirtual.objects.select_related("profesor__usuario").all()
        año = self.request.GET.get("año_curso")
        if año:
            queryset = queryset.filter(año_curso=año)
        return queryset.order_by("año_curso", "profesor__usuario__apellidos")


class AulaCreateView(AdminRequiredMixin, CreateView):
    model = AulaVirtual
    form_class = AulaVirtualForm
    template_name = "admin/aula_form.html"
    success_url = reverse_lazy("academico:aula_list")

    def form_valid(self, form: AulaVirtualForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(self.request, "Aula creada correctamente.")
        return response


class AulaUpdateView(AdminRequiredMixin, UpdateView):
    model = AulaVirtual
    form_class = AulaVirtualForm
    template_name = "admin/aula_form.html"
    success_url = reverse_lazy("academico:aula_list")

    def form_valid(self, form: AulaVirtualForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(self.request, "Aula actualizada correctamente.")
        return response


class AulaDeleteView(AdminRequiredMixin, DeleteView):
    model = AulaVirtual
    template_name = "admin/aula_confirm_delete.html"
    success_url = reverse_lazy("academico:aula_list")

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        messages.success(request, "Aula eliminada correctamente.")
        return super().delete(request, *args, **kwargs)


class UsuarioListView(AdminRequiredMixin, ListView):
    model = Usuario
    template_name = "admin/usuario_list.html"
    context_object_name = "usuarios"
    paginate_by = 10

    def get_queryset(self) -> Any:
        queryset = Usuario.objects.all()
        query = self.request.GET.get("q", "")
        if query:
            queryset = queryset.filter(
                Q(cedula__icontains=query)
                | Q(nombres__icontains=query)
                | Q(apellidos__icontains=query)
                | Q(email__icontains=query)
            )
        return queryset.order_by("apellidos", "nombres")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search_form"] = UsuarioSearchForm(self.request.GET)
        return context


class UsuarioDeleteView(AdminRequiredMixin, DeleteView):
    model = Usuario
    template_name = "admin/usuario_confirm_delete.html"
    success_url = reverse_lazy("academico:usuario_list")

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        messages.success(request, "Usuario eliminado correctamente.")
        return super().delete(request, *args, **kwargs)
