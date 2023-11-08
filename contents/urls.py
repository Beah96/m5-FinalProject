from django.urls import path
from .views import ContentCreate, ContentDetail

urlpatterns = [
    path('courses/<course_id>/contents/', ContentCreate.as_view()),
    path('courses/<course_id>/contents/<content_id>/', ContentDetail.as_view()),
]