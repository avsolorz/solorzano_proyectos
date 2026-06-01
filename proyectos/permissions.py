from rest_framework.permissions import BasePermission, SAFE_METHODS


class EsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.is_staff or getattr(request.user, "rol", None) == "admin")
        )


class EsGestorOAdmin(BasePermission):
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
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.method in SAFE_METHODS
        )
