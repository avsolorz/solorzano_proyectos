from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from proyectos.models import Usuario


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        token["rol"] = user.rol
        token["is_staff"] = user.is_staff
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["usuario"] = {
            "id": self.user.id,
            "username": self.user.username,
            "nombre": self.user.first_name,
            "apellido": self.user.last_name,
            "correo": self.user.email,
            "rol": self.user.rol,
            "es_staff": self.user.is_staff,
        }
        return data


class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, label="Confirmar contraseña")

    class Meta:
        model = Usuario
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "rol",
            "password",
            "password2",
        ]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password2": "Las contraseñas no coinciden."}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = Usuario.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            rol=validated_data.get("rol", Usuario.Rol.COLABORADOR),
            password=validated_data["password"],
        )
        return user


class PerfilUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "rol",
            "is_staff",
            "date_joined",
        ]
        read_only_fields = ["id", "is_staff", "date_joined"]


class CambiarPasswordSerializer(serializers.Serializer):
    password_actual = serializers.CharField(write_only=True)
    password_nuevo = serializers.CharField(write_only=True, min_length=8)
    password_nuevo2 = serializers.CharField(write_only=True, label="Confirmar nueva contraseña")

    def validate(self, data):
        if data["password_nuevo"] != data["password_nuevo2"]:
            raise serializers.ValidationError(
                {"password_nuevo2": "Las contraseñas nuevas no coinciden."}
            )
        return data

    def validate_password_actual(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual es incorrecta.")
        return value

    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["password_nuevo"])
        user.save()
        return user
