from django.contrib import admin

from .models import Actividad, Calificacion, PlanEvaluacion


@admin.register(PlanEvaluacion)
class PlanEvaluacionAdmin(admin.ModelAdmin):
    list_display = ("aula", "lapso", "puntuacion_max", "activo")
    search_fields = ("aula__año_curso", "lapso", "objetivo")
    list_filter = ("activo", "lapso")


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ("titulo", "plan", "fecha", "puntuacion")
    search_fields = ("titulo", "descripcion")
    list_filter = ("fecha", "plan__lapso")


@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ("actividad", "estudiante", "nota_obtenida", "fecha_registro")
    search_fields = ("actividad__titulo", "estudiante__usuario__cedula", "estudiante__usuario__nombres")
    list_filter = ("fecha_registro", "actividad__plan__lapso")
