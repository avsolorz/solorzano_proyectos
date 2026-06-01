from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from proyectos.models import Usuario, Cliente, Evento, Tarea, Proveedor, RedSocial, Disenador


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ["username", "first_name", "last_name", "email", "rol", "is_staff", "is_active"]
    list_filter = ["rol", "is_staff", "is_active"]
    search_fields = ["username", "first_name", "last_name", "email"]
    ordering = ["last_name", "first_name"]
    fieldsets = UserAdmin.fieldsets + (
        ("Rol del sistema", {"fields": ("rol",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Rol del sistema", {"fields": ("rol",)}),
    )


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ["nombre", "telefono", "correo"]
    search_fields = ["nombre", "correo"]
    ordering = ["nombre"]


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ["nombre_evento", "fecha_evento", "ubicacion", "estado", "cliente", "usuario"]
    list_filter = ["estado", "fecha_evento"]
    search_fields = ["nombre_evento", "ubicacion", "cliente__nombre"]
    ordering = ["fecha_evento"]
    date_hierarchy = "fecha_evento"


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ["nombre_tarea", "prioridad", "estado", "fecha_limite", "evento"]
    list_filter = ["prioridad", "estado"]
    search_fields = ["nombre_tarea", "evento__nombre_evento"]
    ordering = ["fecha_limite", "prioridad"]


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ["nombre_empresa", "contacto", "telefono", "correo", "servicio"]
    search_fields = ["nombre_empresa", "servicio", "contacto"]
    ordering = ["nombre_empresa"]


@admin.register(RedSocial)
class RedSocialAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre_red"]
    search_fields = ["nombre_red"]
    ordering = ["nombre_red"]


@admin.register(Disenador)
class DisenadorAdmin(admin.ModelAdmin):
    list_display = ["nombre", "especialidad", "correo", "telefono"]
    search_fields = ["nombre", "correo", "especialidad"]
    ordering = ["nombre"]
