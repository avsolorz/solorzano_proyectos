from django_filters import FilterSet, CharFilter, DateFilter, NumberFilter
from proyectos.models import Cliente, Evento, Tarea, Proveedor


class ClienteFilter(FilterSet):
    nombre = CharFilter(lookup_expr='icontains')
    correo = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Cliente
        fields = ['nombre', 'correo']


class EventoFilter(FilterSet):
    estado = CharFilter(lookup_expr='exact')
    fecha_evento_desde = DateFilter(field_name='fecha_evento', lookup_expr='gte')
    fecha_evento_hasta = DateFilter(field_name='fecha_evento', lookup_expr='lte')
    cliente_nombre = CharFilter(field_name='cliente__nombre', lookup_expr='icontains')
    coordinador_id = NumberFilter(field_name='coordinador__id')

    class Meta:
        model = Evento
        fields = ['estado', 'fecha_evento_desde', 'fecha_evento_hasta',
                  'cliente_nombre', 'coordinador_id']


class TareaFilter(FilterSet):
    estado = CharFilter(lookup_expr='exact')
    prioridad = CharFilter(lookup_expr='exact')
    evento_id = NumberFilter(field_name='evento__id')
    fecha_hasta = DateFilter(field_name='fecha_limite', lookup_expr='lte')

    class Meta:
        model = Tarea
        fields = ['estado', 'prioridad', 'evento_id', 'fecha_hasta']


class ProveedorFilter(FilterSet):
    nombre_empresa = CharFilter(lookup_expr='icontains')
    servicio = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Proveedor
        fields = ['nombre_empresa', 'servicio']
