from rest_framework import serializers
from proyectos.models import Cliente


class ClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        fields = [
            "id",
            "nombre",
            "telefono",
            "correo",
            "direccion",
        ]
        read_only_fields = ["id"]
