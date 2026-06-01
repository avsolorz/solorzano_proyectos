import django_filters
from proyectos.models import Evento, Tarea, RedSocial, Disenador


class EventoFilter(django_filters.FilterSet):
    nombre_evento = django_filters.CharFilter(lookup_expr="icontains")
    estado = django_filters.ChoiceFilter(choices=Evento.Estado.choices)
    cliente = django_filters.NumberFilter(field_name="cliente__id")
    usuario = django_filters.NumberFilter(field_name="usuario__id")
    ubicacion = django_filters.CharFilter(lookup_expr="icontains")
    fecha_desde = django_filters.DateFilter(field_name="fecha_evento", lookup_expr="gte")
    fecha_hasta = django_filters.DateFilter(field_name="fecha_evento", lookup_expr="lte")
    presupuesto_min = django_filters.NumberFilter(field_name="presupuesto", lookup_expr="gte")
    presupuesto_max = django_filters.NumberFilter(field_name="presupuesto", lookup_expr="lte")

    class Meta:
        model = Evento
        fields = [
            "nombre_evento", "estado", "cliente", "usuario",
            "ubicacion", "fecha_desde", "fecha_hasta",
            "presupuesto_min", "presupuesto_max",
        ]


class TareaFilter(django_filters.FilterSet):
    nombre_tarea = django_filters.CharFilter(lookup_expr="icontains")
    estado = django_filters.ChoiceFilter(choices=Tarea.Estado.choices)
    prioridad = django_filters.ChoiceFilter(choices=Tarea.Prioridad.choices)
    evento = django_filters.NumberFilter(field_name="evento__id")
    fecha_limite_desde = django_filters.DateFilter(field_name="fecha_limite", lookup_expr="gte")
    fecha_limite_hasta = django_filters.DateFilter(field_name="fecha_limite", lookup_expr="lte")

    class Meta:
        model = Tarea
        fields = [
            "nombre_tarea", "estado", "prioridad", "evento",
            "fecha_limite_desde", "fecha_limite_hasta",
        ]


class RedSocialFilter(django_filters.FilterSet):
    nombre_red = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = RedSocial
        fields = ["nombre_red"]


class DisenadorFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr="icontains")
    especialidad = django_filters.CharFilter(lookup_expr="icontains")
    correo = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Disenador
        fields = ["nombre", "especialidad", "correo"]
