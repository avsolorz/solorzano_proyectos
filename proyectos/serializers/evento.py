from datetime import date
from rest_framework import serializers
from proyectos.models import Evento, Cliente, Usuario
from proyectos.serializers.cliente import ClienteResumenSerializer
from proyectos.serializers.auth import UsuarioTokenSerializer


class EventoSerializer(serializers.ModelSerializer):
    cliente = ClienteResumenSerializer(read_only=True)
    coordinador = UsuarioTokenSerializer(read_only=True)

    class Meta:
        model = Evento
        fields = '__all__'


class EventoCreateUpdateSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())
    coordinador = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())

    class Meta:
        model = Evento
        fields = '__all__'

    def validate_fecha_evento(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                'La fecha del evento no puede ser en el pasado.'
            )
        return value
