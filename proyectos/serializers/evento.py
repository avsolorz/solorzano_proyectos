from rest_framework import serializers
from proyectos.models import Evento


class EventoSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source="cliente.nombre", read_only=True)
    usuario_nombre = serializers.SerializerMethodField()
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)

    class Meta:
        model = Evento
        fields = [
            "id",
            "nombre_evento",
            "descripcion",
            "fecha_evento",
            "ubicacion",
            "presupuesto",
            "estado",
            "estado_display",
            "cliente",
            "cliente_nombre",
            "usuario",
            "usuario_nombre",
        ]
        read_only_fields = ["id"]

    def get_usuario_nombre(self, obj):
        if obj.usuario:
            return f"{obj.usuario.first_name} {obj.usuario.last_name}".strip()
        return None
