from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from app_usuarios.models import Usuario

from .models import AulaVirtual, Profesor


class AulaVirtualForm(forms.ModelForm):
    año_curso = forms.ChoiceField(choices=[(str(value), str(value)) for value in range(1, 6)], label="Año curso")
    profesor = forms.ModelChoiceField(queryset=Profesor.objects.all(), label="Profesor")
    lapsos = forms.MultipleChoiceField(
        choices=[("I", "I"), ("II", "II"), ("III", "III")],
        widget=forms.CheckboxSelectMultiple,
        label="Lapsos",
        required=False,
    )
    clave_administrativa_confirmacion = forms.CharField(
        label="Clave administrativa de confirmación",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=True,
    )

    class Meta:
        model = AulaVirtual
        fields = ["año_curso", "profesor", "lapsos", "activo"]
        widgets = {
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean(self) -> dict[str, object]:
        cleaned_data = super().clean()
        clave_confirmacion = cleaned_data.get("clave_administrativa_confirmacion", "")
        if isinstance(clave_confirmacion, str):
            clave_confirmacion = clave_confirmacion.strip()
        if clave_confirmacion != settings.CLAVE_ADMINISTRATIVA_MAESTRA:
            raise ValidationError("La clave administrativa de confirmación no es válida.")
        return cleaned_data

    def save(self, commit: bool = True) -> AulaVirtual:
        aula = super().save(commit=False)
        aula.lapsos = list(self.cleaned_data.get("lapsos", []))
        if commit:
            aula.save()
        return aula


class UsuarioSearchForm(forms.Form):
    q = forms.CharField(required=False, label="Buscar", widget=forms.TextInput(attrs={"class": "form-control"}))
