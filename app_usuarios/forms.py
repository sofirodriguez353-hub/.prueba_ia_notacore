from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError

from .models import Usuario


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    clave_administrativa = forms.CharField(
        label="Clave administrativa",
        required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "id": "id_clave_administrativa"}),
    )

    class Meta:
        model = Usuario
        fields = ["cedula", "nombres", "apellidos", "email", "rol", "password1", "password2", "clave_administrativa"]
        widgets = {
            "cedula": forms.TextInput(attrs={"class": "form-control"}),
            "nombres": forms.TextInput(attrs={"class": "form-control"}),
            "apellidos": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "rol": forms.Select(attrs={"class": "form-select", "id": "rol-select"}),
        }
        labels = {
            "cedula": "Cédula",
            "nombres": "Nombres",
            "apellidos": "Apellidos",
            "email": "Correo electrónico",
            "rol": "Rol",
        }

    def clean(self) -> dict[str, object]:
        cleaned_data = super().clean()
        rol = cleaned_data.get("rol")
        if isinstance(rol, str):
            rol = rol.strip().upper()
            cleaned_data["rol"] = rol
        clave_administrativa = cleaned_data.get("clave_administrativa")
        if isinstance(clave_administrativa, str):
            clave_administrativa = clave_administrativa.strip()
            cleaned_data["clave_administrativa"] = clave_administrativa
        roles_requeridos = {Usuario.Rol.ADMIN, Usuario.Rol.PROFESOR}
        if rol in roles_requeridos and not clave_administrativa:
            raise ValidationError("La clave administrativa es obligatoria para este rol.")
        if rol in roles_requeridos and clave_administrativa and clave_administrativa.lower() != settings.CLAVE_ADMINISTRATIVA_MAESTRA.lower():
            raise ValidationError("La clave administrativa no es válida.")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit: bool = True) -> Usuario:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Cédula", widget=forms.TextInput(attrs={"class": "form-control", "autofocus": True}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Cédula"
        self.fields["username"].help_text = ""


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Contraseña actual", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password1 = forms.CharField(label="Nueva contraseña", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password2 = forms.CharField(label="Confirmar nueva contraseña", widget=forms.PasswordInput(attrs={"class": "form-control"}))
