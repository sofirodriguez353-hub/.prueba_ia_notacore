from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        PROFESOR = "PROFESOR", "Profesor"
        ESTUDIANTE = "ESTUDIANTE", "Estudiante"

    cedula: str = models.CharField(primary_key=True, max_length=20)
    nombres: str = models.CharField(max_length=100)
    apellidos: str = models.CharField(max_length=100)
    email: str = models.EmailField(unique=True)
    rol: str = models.CharField(max_length=20, choices=Rol.choices)

    username: str | None = None
    USERNAME_FIELD = "cedula"
    REQUIRED_FIELDS: ClassVar[list[str]] = ["email", "nombres", "apellidos", "rol"]

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self) -> str:
        return f"{self.nombres} {self.apellidos} ({self.cedula})"

    def get_full_name(self) -> str:
        return f"{self.nombres} {self.apellidos}".strip()
