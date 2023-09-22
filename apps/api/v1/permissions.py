from rest_framework.permissions import BasePermission


class IsClientOnly(BasePermission):
    """Доступ только для пользователей с ролью клиент."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_client


class IsPsychologistOnly(BasePermission):
    """Доступ только для пользователей с ролью психолог."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_psychologists


class IsPsychoOwner(IsPsychologistOnly):
    """Доступ к объектам, созданным психологом, только у автора объекта."""
    def has_object_permission(self, request, view, obj):
        return obj.psychologist.user == request.user
