from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):
    """Base permission for YaTube API.
    Allows retrieve objects without authentication.
    """
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class AuthorOrReadOnly(ReadOnly):
    """Allows unsafe requests only for authors.
    Other users are allowed safe requests only.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.author
            or super().has_object_permission(request, view, obj)
        )
