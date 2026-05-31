from django.urls import path
from rest_framework.routers import DefaultRouter
from proyectos.views import (
    UsuarioViewSet,
    ClienteViewSet,
    EventoViewSet,
    TareaViewSet,
    ProveedorViewSet,
    LoginView,
    LogoutView,
    MeView,
    HealthCheckView,
)

router = DefaultRouter()
router.register('usuarios', UsuarioViewSet, basename='usuario')
router.register('clientes', ClienteViewSet, basename='cliente')
router.register('eventos', EventoViewSet, basename='evento')
router.register('tareas', TareaViewSet, basename='tarea')
router.register('proveedores', ProveedorViewSet, basename='proveedor')

urlpatterns = router.urls + [
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('auth/me/', MeView.as_view(), name='auth-me'),
    path('health/', HealthCheckView.as_view(), name='health'),
]
