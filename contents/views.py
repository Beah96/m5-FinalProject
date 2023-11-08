from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView

from courses.models import Course
from .serializers import ContentSerializer
from .models import Content
from .permissions import isStudentOrAdm
from courses.permissions import isAdmOrOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound


class ContentCreate(CreateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[isAdmOrOwner]

    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    def perform_create(self, serializer):
        id=self.kwargs['course_id']
        serializer.save(course_id=id)
        


class ContentDetail(RetrieveUpdateDestroyAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated, isStudentOrAdm]
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    lookup_url_kwarg = 'content_id'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Content.objects.all()
        return Content.objects.filter(course__contents=self.kwargs['content_id'])

    def get_object(self):
        try:
            Course.objects.get(pk=self.kwargs['course_id'])
            content = Content.objects.get(pk=self.kwargs['content_id'])
            self.check_object_permissions(self.request, content)
            return content
        except Course.DoesNotExist:
            raise NotFound({'detail': 'course not found.'})
        except Content.DoesNotExist:
            raise NotFound({'detail': 'content not found.'})