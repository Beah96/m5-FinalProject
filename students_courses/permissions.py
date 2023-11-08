from rest_framework import permissions
from rest_framework.views import View


class isStudent(permissions.BasePermission):
    def has_permission(self, request, view: View):
        return request.user.is_superuser