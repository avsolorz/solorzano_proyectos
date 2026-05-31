from rest_framework.permissions import BasePermission, SAFE_METHODS


class EsAdmin(BasePermission):
    """Solo usuarios con is_staff=True o rol admin tienen acceso total."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.is_staff or getattr(request.user, "rol", None) == "admin")
        )


class EsGestorOAdmin(BasePermission):
    """Gestores y admins pueden crear, editar. No pueden eliminar (solo admin)."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        rol = getattr(request.user, "rol", None)
        if request.user.is_staff or rol == "admin":
            return True
        if request.method == "DELETE":
            return False
        return rol in ("gestor", "admin")


class SoloLectura(BasePermission):
    """Permite solo métodos seguros (GET, HEAD, OPTIONS) a usuarios autenticados."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.method in SAFE_METHODS
        )
