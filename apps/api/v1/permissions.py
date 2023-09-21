from rest_framework.permissions import BasePermission


class IsClientOnly(BasePermission):
    """Доступ только для пользователей с ролью клиент."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_client
