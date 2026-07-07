from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, View

from .forms import CustomPasswordChangeForm, LoginForm, SignupForm
from .models import Usuario


class SignupView(CreateView):
    model = Usuario
    form_class = SignupForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("usuarios:login")

    def form_valid(self, form: SignupForm) -> object:
        response = super().form_valid(form)
        messages.success(self.request, "Registro realizado con éxito. Ya puedes iniciar sesión.")
        return response

    def form_invalid(self, form: SignupForm) -> object:
        messages.error(self.request, "No se pudo completar el registro. Revise los datos ingresados.")
        return super().form_invalid(form)


class LoginView(FormView):
    template_name = "registration/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("usuarios:login")

    def form_valid(self, form: LoginForm) -> object:
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, f"Bienvenido, {user.get_full_name() or user.cedula}.")
        if user.rol == Usuario.Rol.ADMIN:
            return redirect("dashboard_admin")
        if user.rol == Usuario.Rol.PROFESOR:
            return redirect("dashboard_profesor")
        return redirect("dashboard_estudiante")


class LogoutView(View):
    def get(self, request: object, *args: object, **kwargs: object) -> object:
        logout(request)
        messages.info(request, "Sesión cerrada correctamente.")
        return redirect("usuarios:login")

    def post(self, request: object, *args: object, **kwargs: object) -> object:
        logout(request)
        messages.info(request, "Sesión cerrada correctamente.")
        return redirect("usuarios:login")


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "registration/password_change_form.html"
    success_url = reverse_lazy("usuarios:password_change_done")
    form_class = CustomPasswordChangeForm

    def form_valid(self, form: CustomPasswordChangeForm) -> object:
        response = super().form_valid(form)
        messages.success(self.request, "La contraseña se cambió correctamente.")
        return response

    def form_invalid(self, form: CustomPasswordChangeForm) -> object:
        messages.error(self.request, "No se pudo cambiar la contraseña. Revise los datos ingresados.")
        return super().form_invalid(form)
