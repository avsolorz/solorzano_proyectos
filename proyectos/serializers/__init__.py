from proyectos.serializers.auth import LoginSerializer, UsuarioTokenSerializer
from proyectos.serializers.usuario import (
    UsuarioSerializer,
    UsuarioCreateSerializer,
    UsuarioCambiarRolSerializer,
)
from proyectos.serializers.cliente import ClienteSerializer, ClienteResumenSerializer
from proyectos.serializers.evento import EventoSerializer, EventoCreateUpdateSerializer
from proyectos.serializers.tarea import TareaSerializer, TareaCambiarEstadoSerializer
from proyectos.serializers.proveedor import ProveedorSerializer

__all__ = [
    'LoginSerializer',
    'UsuarioTokenSerializer',
    'UsuarioSerializer',
    'UsuarioCreateSerializer',
    'UsuarioCambiarRolSerializer',
    'ClienteSerializer',
    'ClienteResumenSerializer',
    'EventoSerializer',
    'EventoCreateUpdateSerializer',
    'TareaSerializer',
    'TareaCambiarEstadoSerializer',
    'ProveedorSerializer',
]
