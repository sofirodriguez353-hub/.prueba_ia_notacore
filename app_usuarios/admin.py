from django.contrib import admin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("cedula", "nombres", "apellidos", "email", "rol", "is_active")
    search_fields = ("cedula", "nombres", "apellidos", "email")
    list_filter = ("rol", "is_active")
