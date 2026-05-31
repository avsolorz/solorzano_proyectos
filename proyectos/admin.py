from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from proyectos.models import Usuario, Cliente, Evento, Tarea, Proveedor


class TareaInline(admin.TabularInline):
    model = Tarea
    extra = 1
    fields = ['nombre_tarea', 'prioridad', 'estado', 'fecha_limite']


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['correo', 'nombre', 'apellido', 'rol', 'is_active']
    list_filter = ['rol', 'is_active']
    search_fields = ['correo', 'nombre', 'apellido']
    ordering = ['correo']
    fieldsets = (
        ('Información personal', {'fields': ('correo', 'nombre', 'apellido', 'password')}),
        ('Permisos', {'fields': ('rol', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('correo', 'nombre', 'apellido', 'rol', 'password1', 'password2'),
        }),
    )


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'correo', 'telefono']
    search_fields = ['nombre', 'correo']


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['nombre_evento', 'estado', 'fecha_evento', 'cliente', 'coordinador', 'presupuesto']
    list_filter = ['estado', 'fecha_evento']
    search_fields = ['nombre_evento', 'cliente__nombre', 'coordinador__correo']
    inlines = [TareaInline]


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['nombre_tarea', 'prioridad', 'estado', 'fecha_limite', 'evento']
    list_filter = ['estado', 'prioridad']
    search_fields = ['nombre_tarea', 'evento__nombre_evento']


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre_empresa', 'servicio', 'correo', 'telefono']
    search_fields = ['nombre_empresa', 'servicio']
