from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Ограничение доступа. Для Админа."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    """Ограничение доступа. Для Админа, Модератора, Владельца."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)


class IsAdmin(permissions.BasePermission):
    """Ограниечение доступа. Для доступа Админу."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)