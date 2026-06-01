from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from proyectos.models import RedSocial
from proyectos.serializers import RedSocialSerializer
from proyectos.permissions import EsAdmin
from proyectos.filters import RedSocialFilter


class RedSocialViewSet(viewsets.ModelViewSet):
    queryset = RedSocial.objects.all()
    serializer_class = RedSocialSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = RedSocialFilter
    search_fields = ["nombre_red"]
    ordering_fields = ["nombre_red"]
    ordering = ["nombre_red"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAuthenticated(), EsAdmin()]
