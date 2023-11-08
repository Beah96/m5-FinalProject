from django.urls import path
from .views import StudentsCoursesView

urlpatterns = [
    path('courses/<course_id>/students/', StudentsCoursesView.as_view())
]