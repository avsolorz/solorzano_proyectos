from rest_framework.permissions import BasePermission


class EsAdmin(BasePermission):
    message = 'Se requiere rol de administrador.'

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.rol == 'admin'
        )


class EsCoordinador(BasePermission):
    message = 'Se requiere rol de coordinador o administrador.'

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.rol in ['admin', 'coordinador']
        )


class EsPropietarioOAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.rol == 'admin' or
            obj.coordinador == request.user
        )
