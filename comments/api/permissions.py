from rest_framework.permissions import BasePermission

class IsObjectOwner(BasePermission):
    """
    authentication class by checking the obj.user == request.user
    """
    default_message = "You do not have permission to access this object"
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user