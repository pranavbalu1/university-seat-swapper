from rest_framework import serializers # type: ignore
from django.contrib.auth.models import User # type: ignore
from .models import StudentProfile, StudentClass 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['user', 'student_id', 'full_name', 'email']


class StudentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = ['id', 'course_number', 'section_number', 'class_name', 'instructor', 'start_time', 'days']
