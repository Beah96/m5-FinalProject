from .models import Course
from .serializers import CourseSerializer 
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .permissions import isAdmOrOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404


class CourseView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isAdmOrOwner]
    serializer_class = CourseSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Course.objects.all()
        
        return Course.objects.filter(students=self.request.user)

class CourseDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isAdmOrOwner]
    serializer_class = CourseSerializer
    lookup_url_kwarg = 'course_id'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Course.objects.all() 
        
        return Course.objects.filter(students=self.request.user)
    
    def get_object(self):
        return get_object_or_404(Course, id=self.kwargs['course_id'])


        



