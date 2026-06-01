from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from proyectos.models import Disenador
from proyectos.serializers import DisenadorSerializer
from proyectos.permissions import EsAdmin
from proyectos.filters import DisenadorFilter


class DisenadorViewSet(viewsets.ModelViewSet):
    queryset = Disenador.objects.all()
    serializer_class = DisenadorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DisenadorFilter
    search_fields = ["nombre", "especialidad", "correo"]
    ordering_fields = ["nombre", "especialidad"]
    ordering = ["nombre"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAuthenticated(), EsAdmin()]
