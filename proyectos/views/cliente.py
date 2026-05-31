from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from proyectos.models import Cliente
from proyectos.serializers import ClienteSerializer
from proyectos.permissions import EsGestorOAdmin, SoloLectura


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["nombre"]
    search_fields = ["nombre", "correo", "telefono"]
    ordering_fields = ["nombre"]
    ordering = ["nombre"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [SoloLectura()]
        return [EsGestorOAdmin()]
