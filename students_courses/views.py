from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from courses.models import Course
from .serializers import PutStudentsCoursesSerializer
from .permissions import isStudent


class StudentsCoursesView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isStudent]
    serializer_class = PutStudentsCoursesSerializer
    lookup_url_kwarg = 'course_id'
    queryset = Course.objects.all()

   
    
    