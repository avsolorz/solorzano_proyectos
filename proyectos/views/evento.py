from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from proyectos.models import Evento
from proyectos.serializers import EventoSerializer
from proyectos.permissions import EsGestorOAdmin, SoloLectura
from proyectos.filters import EventoFilter


class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.select_related("cliente", "usuario").all()
    serializer_class = EventoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EventoFilter
    search_fields = ["nombre_evento", "ubicacion", "cliente__nombre"]
    ordering_fields = ["fecha_evento", "nombre_evento", "presupuesto"]
    ordering = ["fecha_evento"]

    def get_permissions(self):
        if self.action in ["list", "retrieve", "por_cliente"]:
            return [SoloLectura()]
        return [EsGestorOAdmin()]

    @action(detail=True, methods=["patch"], url_path="cambiar-estado")
    def cambiar_estado(self, request, pk=None):
        """PATCH /api/eventos/{id}/cambiar-estado/"""
        evento = self.get_object()
        nuevo_estado = request.data.get("estado")
        estados_validos = [e[0] for e in Evento.Estado.choices]
        if nuevo_estado not in estados_validos:
            return Response(
                {"error": f"Estado inválido. Opciones: {estados_validos}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        evento.estado = nuevo_estado
        evento.save()
        return Response(self.get_serializer(evento).data)

    @action(detail=False, methods=["get"], url_path="por-cliente")
    def por_cliente(self, request):
        """GET /api/eventos/por-cliente/?cliente_id=1"""
        cliente_id = request.query_params.get("cliente_id")
        if not cliente_id:
            return Response(
                {"error": "Se requiere el parámetro 'cliente_id'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        eventos = self.get_queryset().filter(cliente_id=cliente_id)
        return Response(self.get_serializer(eventos, many=True).data)
