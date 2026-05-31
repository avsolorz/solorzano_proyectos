from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from proyectos.models import Proveedor
from proyectos.serializers import ProveedorSerializer
from proyectos.permissions import EsGestorOAdmin, SoloLectura


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["servicio"]
    search_fields = ["nombre_empresa", "contacto", "servicio", "correo"]
    ordering_fields = ["nombre_empresa", "servicio"]
    ordering = ["nombre_empresa"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [SoloLectura()]
        return [EsGestorOAdmin()]
