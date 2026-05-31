from rest_framework import serializers
from proyectos.models import Tarea


class TareaSerializer(serializers.ModelSerializer):
    evento_nombre = serializers.CharField(source="evento.nombre_evento", read_only=True)
    prioridad_display = serializers.CharField(source="get_prioridad_display", read_only=True)
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)

    class Meta:
        model = Tarea
        fields = [
            "id",
            "nombre_tarea",
            "descripcion",
            "fecha_limite",
            "prioridad",
            "prioridad_display",
            "estado",
            "estado_display",
            "evento",
            "evento_nombre",
        ]
        read_only_fields = ["id"]
