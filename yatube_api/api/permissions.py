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
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class FollowObjectPermission(permissions.BasePermission):
    """
    Запрещает запросы пользователя к чужим подпискам.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
