from rest_framework import serializers
from proyectos.models import Disenador


class DisenadorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Disenador
        fields = ["id", "nombre", "especialidad", "telefono", "correo"]
        read_only_fields = ["id"]


class DisenadorResumenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Disenador
        fields = ["id", "nombre", "especialidad"]
        read_only_fields = ["id"]
