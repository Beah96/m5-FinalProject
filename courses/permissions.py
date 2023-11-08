from rest_framework import permissions
from rest_framework.views import Request, View

class isAdmOrOwner(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return(
            request.user.is_superuser
            or request.method in permissions.SAFE_METHODS
        )
    
