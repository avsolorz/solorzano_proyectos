from django.urls import path, include
from rest_framework.routers import DefaultRouter
from proyectos.views import (
    UsuarioViewSet, ClienteViewSet, EventoViewSet,
    TareaViewSet, ProveedorViewSet, health_check,
    LoginView, RefreshTokenView, RegistroView,
    logout_view, PerfilView, cambiar_password,
)

router = DefaultRouter()
router.register("usuarios", UsuarioViewSet, basename="usuario")
router.register("clientes", ClienteViewSet, basename="cliente")
router.register("eventos", EventoViewSet, basename="evento")
router.register("tareas", TareaViewSet, basename="tarea")
router.register("proveedores", ProveedorViewSet, basename="proveedor")

auth_urlpatterns = [
    path("login/",            LoginView.as_view(),        name="auth-login"),
    path("refresh/",          RefreshTokenView.as_view(), name="auth-refresh"),
    path("registro/",         RegistroView.as_view(),     name="auth-registro"),
    path("logout/",           logout_view,                name="auth-logout"),
    path("perfil/",           PerfilView.as_view(),       name="auth-perfil"),
    path("cambiar-password/", cambiar_password,           name="auth-cambiar-password"),
]

urlpatterns = [
    path("health/", health_check, name="health"),
    path("auth/", include(auth_urlpatterns)),
    path("", include(router.urls)),
]
