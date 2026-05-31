from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from proyectos.models import Proveedor
from proyectos.serializers import ProveedorSerializer
from proyectos.filters import ProveedorFilter
from proyectos.permissions import EsAdmin


class ProveedorViewSet(ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    filterset_class = ProveedorFilter

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), EsAdmin()]
