from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Запрет PUT/PATCH/DELETE запросов для не автора поста,
    запрет POST запроса для гостя.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

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
