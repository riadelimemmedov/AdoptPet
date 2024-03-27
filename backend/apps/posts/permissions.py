from rest_framework import permissions


# *IsAuthorOrReadOnly
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Check if authenticated user is author of the post.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated is True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # GET,OPTIONS,HEAD
            return True
        # If request equal to POST,PUT,PATCH,DELETE
        return obj.author == request.user
