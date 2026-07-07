from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Sum

from app_academico.models import AulaVirtual, Estudiante, Matricula
from app_usuarios.models import Usuario

from .models import Actividad, Calificacion, PlanEvaluacion


class PlanEvaluacionForm(forms.ModelForm):
    class Meta:
        model = PlanEvaluacion
        fields = ["aula", "lapso", "objetivo", "metodo", "puntuacion_max"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.fields["aula"].queryset = self.get_profesor_aulas()
        if self.instance.pk and self.instance.aula_id:
            self.fields["aula"].initial = self.instance.aula
        elif self.fields["aula"].queryset.exists():
            self.fields["aula"].initial = self.fields["aula"].queryset.first()

    def get_profesor_aulas(self):
        if not self.request or not self.request.user.is_authenticated:
            return AulaVirtual.objects.none()
        if self.request.user.rol != Usuario.Rol.PROFESOR:
            return AulaVirtual.objects.none()
        return AulaVirtual.objects.filter(profesor__usuario=self.request.user).order_by("año_curso")

    def clean(self):
        cleaned_data = super().clean()
        puntuacion_max = cleaned_data.get("puntuacion_max")
        aula = cleaned_data.get("aula")
        lapso = cleaned_data.get("lapso")

        if puntuacion_max is None or aula is None or lapso is None:
            return cleaned_data

        if puntuacion_max > Decimal("20.00"):
            raise forms.ValidationError("La puntuación máxima no puede superar los 20 puntos.")

        queryset = PlanEvaluacion.objects.filter(aula=aula, lapso=lapso, activo=True)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        acumulado = queryset.aggregate(total=Sum("puntuacion_max"))["total"] or Decimal("0.00")
        if acumulado + puntuacion_max > Decimal("20.00"):
            raise forms.ValidationError(
                "La suma de los planes activos del mismo aula y lapso no puede exceder los 20 puntos acumulados."
            )

        return cleaned_data


class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ["plan", "titulo", "fecha", "puntuacion", "descripcion"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.plan = kwargs.pop("plan", None)
        super().__init__(*args, **kwargs)
        self.fields["plan"].queryset = self.get_planes_profesor()
        if self.plan is not None:
            self.fields["plan"].initial = self.plan

    def get_planes_profesor(self):
        if not self.request or not self.request.user.is_authenticated:
            return PlanEvaluacion.objects.none()
        if self.request.user.rol != Usuario.Rol.PROFESOR:
            return PlanEvaluacion.objects.none()
        return PlanEvaluacion.objects.filter(aula__profesor__usuario=self.request.user).order_by("aula__año_curso", "lapso")

    def clean(self):
        cleaned_data = super().clean()
        plan = cleaned_data.get("plan")
        puntuacion = cleaned_data.get("puntuacion")

        if plan and puntuacion is not None and puntuacion > plan.puntuacion_max:
            raise forms.ValidationError("La puntuación de la actividad no puede superar la puntuación máxima del plan.")

        return cleaned_data


class AsignarEstudianteForm(forms.Form):
    cedula_estudiante = forms.CharField(label="Cédula del estudiante", max_length=20)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean_cedula_estudiante(self):
        cedula = self.cleaned_data["cedula_estudiante"].strip()
        try:
            estudiante = Estudiante.objects.select_related("usuario").get(usuario__cedula=cedula)
        except Estudiante.DoesNotExist as exc:
            raise forms.ValidationError("No existe un estudiante con esa cédula.") from exc
        return cedula

    def save(self):
        if not self.request or not self.request.user.is_authenticated:
            raise ValidationError("Debe iniciar sesión para asignar estudiantes.")

        aula = AulaVirtual.objects.filter(profesor__usuario=self.request.user).order_by("año_curso").first()
        if aula is None:
            raise ValidationError("No tiene un aula asignada para matricular estudiantes.")

        estudiante = Estudiante.objects.select_related("usuario").get(usuario__cedula=self.cleaned_data["cedula_estudiante"].strip())
        matricula, created = Matricula.objects.get_or_create(estudiante=estudiante, aula=aula)
        return matricula, created


class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ["nota_obtenida", "observacion"]

    def clean(self):
        cleaned_data = super().clean()
        nota_obtenida = cleaned_data.get("nota_obtenida")
        actividad = getattr(self.instance, "actividad", None)

        if actividad and nota_obtenida is not None and nota_obtenida > actividad.puntuacion:
            raise forms.ValidationError("La nota obtenida no puede superar la puntuación de la actividad.")

        return cleaned_data
