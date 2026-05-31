from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from proyectos.models import Tarea
from proyectos.serializers import TareaSerializer, TareaCambiarEstadoSerializer
from proyectos.filters import TareaFilter
from proyectos.permissions import EsCoordinador


class TareaViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, EsCoordinador]
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
    filterset_class = TareaFilter

    @action(methods=['patch'], detail=True, url_path='cambiar-estado')
    def cambiar_estado(self, request, pk=None):
        tarea = self.get_object()
        serializer = TareaCambiarEstadoSerializer(tarea, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(TareaSerializer(tarea).data)
