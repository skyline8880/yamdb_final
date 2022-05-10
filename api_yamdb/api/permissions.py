from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return (request.user and request.user.is_authenticated
                and request.user.is_admin)


class ReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):

        return (request.method in permissions.SAFE_METHODS
                or request.user
                and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            if (request.user.is_staff or request.user.is_admin
                    or request.user.is_moderator
                    or obj.author == request.user
                    or request.method == 'POST'
                    and request.user.is_authenticated):
                return True
            else:
                return False
        elif request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False
