from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешение на уровне объектов: только автор может редактировать."""

    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS разрешены всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # DELETE, PUT, PATCH только автору
        return obj.author == request.user
