from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from proyectos.models import Evento
from proyectos.serializers import (
    EventoSerializer,
    EventoCreateUpdateSerializer,
    TareaSerializer,
)
from proyectos.filters import EventoFilter
from proyectos.permissions import EsCoordinador, EsPropietarioOAdmin
from proyectos.pagination import CustomPagination


class EventoViewSet(ModelViewSet):
    filterset_class = EventoFilter

    def get_queryset(self):
        usuario = self.request.user
        if usuario.rol == 'admin':
            return Evento.objects.all()
        return Evento.objects.filter(coordinador=usuario)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EventoCreateUpdateSerializer
        return EventoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            return [IsAuthenticated(), EsCoordinador()]
        return [IsAuthenticated(), EsPropietarioOAdmin()]

    @action(methods=['get'], detail=True, url_path='tareas')
    def tareas(self, request, pk=None):
        evento = self.get_object()
        tareas_qs = evento.tareas.all()
        paginator = CustomPagination()
        page = paginator.paginate_queryset(tareas_qs, request)
        if page is not None:
            serializer = TareaSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = TareaSerializer(tareas_qs, many=True)
        return Response(serializer.data)
