from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    correo = serializers.EmailField(label='Correo electrónico')
    contrasena = serializers.CharField(
        label='Contraseña',
        write_only=True,
        style={'input_type': 'password'},
    )

    def validate(self, data):
        correo = data.get('correo')
        contrasena = data.get('contrasena')

        usuario = authenticate(
            request=self.context.get('request'),
            username=correo,
            password=contrasena,
        )
        if not usuario:
            raise serializers.ValidationError('Credenciales inválidas.')

        if not usuario.is_active:
            raise serializers.ValidationError('Esta cuenta está inactiva.')

        data['usuario'] = usuario
        return data


class UsuarioTokenSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    correo = serializers.EmailField(read_only=True)
    nombre = serializers.CharField(read_only=True)
    apellido = serializers.CharField(read_only=True)
    rol = serializers.CharField(read_only=True)
