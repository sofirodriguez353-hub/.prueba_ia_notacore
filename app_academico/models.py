from typing import ClassVar

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from app_usuarios.models import Usuario


class Profesor(models.Model):
    usuario: Usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={"rol": Usuario.Rol.PROFESOR},
        related_name="profesor",
    )

    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"

    def __str__(self) -> str:
        return str(self.usuario)


class Estudiante(models.Model):
    usuario: Usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={"rol": Usuario.Rol.ESTUDIANTE},
        related_name="estudiante",
    )
    representante: str = models.CharField(max_length=150)
    telefono_representante: str = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

    def __str__(self) -> str:
        return str(self.usuario)


class AulaVirtual(models.Model):
    class Lapso(models.TextChoices):
        I = "I", "I"
        II = "II", "II"
        III = "III", "III"

    año_curso: int = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    lapsos: list[str] = models.JSONField(default=list)
    profesor: Profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name="aulas")
    activo: bool = models.BooleanField(default=True)
    fecha_creacion: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Aula Virtual"
        verbose_name_plural = "Aulas Virtuales"

    def __str__(self) -> str:
        return f"Aula {self.año_curso} - {self.profesor}"


class Matricula(models.Model):
    estudiante: Estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="matriculas")
    aula: AulaVirtual = models.ForeignKey(AulaVirtual, on_delete=models.CASCADE, related_name="matriculas")
    fecha_inscripcion: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        constraints: ClassVar[list[models.BaseConstraint]] = [
            models.UniqueConstraint(fields=["estudiante", "aula"], name="unique_matricula_estudiante_aula")
        ]

    def __str__(self) -> str:
        return f"{self.estudiante} -> {self.aula}"
