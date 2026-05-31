from proyectos.views.health import HealthCheckView
from proyectos.views.auth import LoginView, LogoutView, MeView
from proyectos.views.usuario import UsuarioViewSet
from proyectos.views.cliente import ClienteViewSet
from proyectos.views.evento import EventoViewSet
from proyectos.views.tarea import TareaViewSet
from proyectos.views.proveedor import ProveedorViewSet

__all__ = [
    'HealthCheckView',
    'LoginView',
    'LogoutView',
    'MeView',
    'UsuarioViewSet',
    'ClienteViewSet',
    'EventoViewSet',
    'TareaViewSet',
    'ProveedorViewSet',
]
