from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from proyectos.models import Usuario
from proyectos.serializers import UsuarioSerializer
from proyectos.permissions import EsAdmin


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["rol", "is_active", "is_staff"]
    search_fields = ["username", "first_name", "last_name", "email"]
    ordering_fields = ["last_name", "first_name", "date_joined"]
    ordering = ["last_name"]

    def get_permissions(self):
        return [EsAdmin()]
