from django.contrib import admin

from .models import AulaVirtual, Estudiante, Matricula, Profesor


@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ("usuario",)
    search_fields = ("usuario__cedula", "usuario__nombres", "usuario__apellidos")


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ("usuario", "representante", "telefono_representante")
    search_fields = ("usuario__cedula", "usuario__nombres", "usuario__apellidos", "representante")
    list_filter = ("usuario__rol",)


@admin.register(AulaVirtual)
class AulaVirtualAdmin(admin.ModelAdmin):
    list_display = ("año_curso", "profesor", "activo", "fecha_creacion")
    search_fields = ("año_curso", "profesor__usuario__nombres", "profesor__usuario__apellidos")
    list_filter = ("activo", "año_curso")


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ("estudiante", "aula", "fecha_inscripcion")
    search_fields = ("estudiante__usuario__cedula", "aula__año_curso")
    list_filter = ("aula__año_curso", "fecha_inscripcion")
