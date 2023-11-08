from rest_framework import serializers
from .models import StudentCourse
from courses.models import Course
from accounts.models import Account
from rest_framework.exceptions import ParseError


class StudentsCoursesSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    student_email = serializers.CharField(source='student.email')
    class Meta:
        model = StudentCourse
        fields = [
            'id', 
            'status', 
            'student_id',
            'student_username', 
            'student_email'
        ]
        read_only_fields = [
            'student_id'
        ]

class PutStudentsCoursesSerializer(serializers.ModelSerializer):
    students_courses = StudentsCoursesSerializer(many=True)
    class Meta:
        model = Course
        fields = ['id', 'name', 'students_courses']
        depth = 1
        read_only_fields = ['id', 'name']
    
    def update(self, instance, validated_data):
        for user in validated_data['students_courses']:
            email = user['student']['email']
            account = Account.objects.filter(email=email).first()
            if not account:
                raise ParseError({'detail': f'No active accounts was found: {email}.'})
            instance.students.add(account) 
        instance.save()
        return instance

