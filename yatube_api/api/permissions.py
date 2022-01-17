from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Ограничение прав на PUT/PATCH/DELETE запросы,
    если юзер не владелец записей.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class FollowObjectPermission(permissions.BasePermission):
    """
    Запрет на PUT/PATCH запросы к модели Follow,
    проверка прав при DELETE запросе
    и запрет просмотра чужой подписки.
    """
    def has_permission(self, request, view):
        return request.method not in ('PUT', 'PATCH')

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user == obj.user
        return request.user == obj.user
