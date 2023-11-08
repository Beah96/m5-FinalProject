from contents.serializers import ContentSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'status',
            'start_date',
            'end_date',
            'instructor',
            'contents',
            'students_courses'
        ]
        extra_kwargs = {
            'students_courses': {
                'source': 'students'
            },
            'name': {
                'validators': [
                    UniqueValidator(
                        queryset=Course.objects.all(),
                        message='course with this name already exists.'
                    )
                ]
            }
        }

