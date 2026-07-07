from decimal import Decimal
from typing import ClassVar

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

from app_academico.models import AulaVirtual, Estudiante


class PlanEvaluacion(models.Model):
    class Lapso(models.TextChoices):
        I = "I", "I"
        II = "II", "II"
        III = "III", "III"

    aula: AulaVirtual = models.ForeignKey(AulaVirtual, on_delete=models.CASCADE, related_name="planes_evaluacion")
    lapso: str = models.CharField(max_length=5, choices=Lapso.choices)
    objetivo: str = models.TextField()
    metodo: str = models.CharField(max_length=100)
    puntuacion_max: Decimal = models.DecimalField(max_digits=5, decimal_places=2, validators=[MaxValueValidator(Decimal("20.00"))])
    activo: bool = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Plan de Evaluación"
        verbose_name_plural = "Planes de Evaluación"

    def __str__(self) -> str:
        return f"Plan {self.aula} - {self.lapso}"


class Actividad(models.Model):
    plan: PlanEvaluacion = models.ForeignKey(PlanEvaluacion, on_delete=models.CASCADE, related_name="actividades")
    titulo: str = models.CharField(max_length=150)
    fecha: models.DateField = models.DateField()
    puntuacion: Decimal = models.DecimalField(max_digits=5, decimal_places=2)
    descripcion: str = models.TextField(blank=True)

    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"

    def clean(self) -> None:
        super().clean()
        if self.plan_id and self.puntuacion > self.plan.puntuacion_max:
            raise ValidationError({"puntuacion": "La puntuación de la actividad no puede superar la puntuación máxima del plan."})

    def save(self, *args: object, **kwargs: object) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.titulo


class Calificacion(models.Model):
    actividad: Actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name="calificaciones")
    estudiante: Estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="calificaciones")
    nota_obtenida: Decimal = models.DecimalField(max_digits=5, decimal_places=2)
    observacion: str = models.TextField(blank=True)
    fecha_registro: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(fields=["actividad", "estudiante"], name="unique_calificacion_actividad_estudiante"),
        ]

    def clean(self) -> None:
        super().clean()
        if self.actividad_id and self.nota_obtenida > self.actividad.plan.puntuacion_max:
            raise ValidationError({"nota_obtenida": "La nota obtenida no puede superar la puntuación máxima del plan."})

    def save(self, *args: object, **kwargs: object) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.estudiante} - {self.actividad}"
