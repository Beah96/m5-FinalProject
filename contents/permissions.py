from rest_framework import permissions
from rest_framework.views import View
from .models import Content


class isStudentOrAdm(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj:Content ):

        return (
            request.user.is_superuser or
            request.method in permissions.SAFE_METHODS
            and request.user in obj.course.students.all()
        )