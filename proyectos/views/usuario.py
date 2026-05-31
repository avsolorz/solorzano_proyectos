from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from proyectos.models import Usuario
from proyectos.serializers import (
    UsuarioSerializer,
    UsuarioCreateSerializer,
    UsuarioCambiarRolSerializer,
)
from proyectos.permissions import EsAdmin


class UsuarioViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, EsAdmin]
    queryset = Usuario.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UsuarioCreateSerializer
        return UsuarioSerializer

    @action(methods=['post'], detail=True, url_path='cambiar-rol')
    def cambiar_rol(self, request, pk=None):
        usuario = self.get_object()
        serializer = UsuarioCambiarRolSerializer(usuario, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UsuarioSerializer(usuario).data)
