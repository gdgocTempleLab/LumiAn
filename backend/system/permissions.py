from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    """
    Custom permission to only allow users with the 'Admin' role to access.
    """
    def has_permission(self, request, view):
        # Ensure the user is authenticated and their role is 'Admin'
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'role', None) == 'Admin')
