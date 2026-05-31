from rest_framework import serializers
from proyectos.models import Tarea


class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'

    def validate(self, data):
        fecha_limite = data.get('fecha_limite')
        evento = data.get('evento')

        if fecha_limite and evento:
            if fecha_limite < evento.fecha_evento:
                raise serializers.ValidationError(
                    'La fecha límite no puede ser anterior a la fecha del evento.'
                )
        return data


class TareaCambiarEstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ['estado']
