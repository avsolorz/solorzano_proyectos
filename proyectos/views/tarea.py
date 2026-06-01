from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from proyectos.models import Tarea
from proyectos.serializers import TareaSerializer
from proyectos.permissions import EsGestorOAdmin, SoloLectura
from proyectos.filters import TareaFilter


class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.select_related("evento").all()
    serializer_class = TareaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TareaFilter
    search_fields = ["nombre_tarea", "descripcion"]
    ordering_fields = ["fecha_limite", "prioridad", "estado"]
    ordering = ["fecha_limite"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [SoloLectura()]
        return [EsGestorOAdmin()]

    @action(detail=True, methods=["patch"], url_path="cambiar-estado")
    def cambiar_estado(self, request, pk=None):
        tarea = self.get_object()
        nuevo_estado = request.data.get("estado")
        estados_validos = [e[0] for e in Tarea.Estado.choices]
        if nuevo_estado not in estados_validos:
            return Response(
                {"error": f"Estado inválido. Opciones: {estados_validos}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        tarea.estado = nuevo_estado
        tarea.save()
        return Response(self.get_serializer(tarea).data)
