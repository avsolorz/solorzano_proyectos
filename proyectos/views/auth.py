from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from proyectos.models import Usuario
from proyectos.serializers.auth import (
    CustomTokenObtainPairSerializer,
    RegistroUsuarioSerializer,
    PerfilUsuarioSerializer,
    CambiarPasswordSerializer,
)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class RefreshTokenView(TokenRefreshView):
    permission_classes = [AllowAny]


class RegistroView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroUsuarioSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "mensaje": "Usuario creado exitosamente.",
                "usuario": {
                    "id": user.id,
                    "username": user.username,
                    "correo": user.email,
                    "rol": user.rol,
                },
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"error": "Se requiere el refresh token."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"mensaje": "Sesión cerrada exitosamente."})
    except Exception:
        return Response(
            {"error": "Token inválido o ya expirado."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class PerfilView(generics.RetrieveUpdateAPIView):
    serializer_class = PerfilUsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cambiar_password(request):
    serializer = CambiarPasswordSerializer(
        data=request.data, context={"request": request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje": "Contraseña actualizada exitosamente."})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
