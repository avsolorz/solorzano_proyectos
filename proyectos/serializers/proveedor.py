from rest_framework import serializers
from proyectos.models import Proveedor


class ProveedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proveedor
        fields = [
            "id",
            "nombre_empresa",
            "contacto",
            "telefono",
            "correo",
            "servicio",
        ]
        read_only_fields = ["id"]
