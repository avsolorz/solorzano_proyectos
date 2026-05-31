from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from proyectos.models import Cliente
from proyectos.serializers import ClienteSerializer
from proyectos.filters import ClienteFilter
from proyectos.permissions import EsAdmin, EsCoordinador


class ClienteViewSet(ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filterset_class = ClienteFilter

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), EsCoordinador()]
        return [IsAuthenticated(), EsAdmin()]
