from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Кастомный пермишен для PUT/PATCH/DELETE запросов."""
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class FollowPermission(permissions.BasePermission):
    """Запрет PUT/PATCH запросов к модели Follow."""
    def has_permission(self, request, view):
        if request.method not in ('PUT', 'PATCH'):
            return True
        return False