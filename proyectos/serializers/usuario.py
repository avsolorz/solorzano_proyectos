from rest_framework import serializers
from proyectos.models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'correo', 'nombre', 'apellido', 'rol', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UsuarioCreateSerializer(serializers.ModelSerializer):
    contrasena = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
        label='Contraseña',
    )

    class Meta:
        model = Usuario
        fields = ['id', 'correo', 'nombre', 'apellido', 'rol', 'contrasena']
        read_only_fields = ['id']

    def create(self, validated_data):
        contrasena = validated_data.pop('contrasena')
        usuario = Usuario(**validated_data)
        usuario.set_password(contrasena)
        usuario.save()
        return usuario


class UsuarioCambiarRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['rol']

    def validate_rol(self, value):
        roles_validos = [r[0] for r in Usuario.ROL_CHOICES]
        if value not in roles_validos:
            raise serializers.ValidationError(
                f"Rol inválido. Opciones válidas: {', '.join(roles_validos)}"
            )
        return value
