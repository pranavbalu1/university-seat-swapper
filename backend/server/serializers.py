from rest_framework import serializers # type: ignore
from django.contrib.auth.models import User # type: ignore
from .models import StudentProfile, StudentClass, ClassTradeRequest
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


class ClassTradeRequestSerializer(serializers.ModelSerializer):
    offered_class = StudentClassSerializer(read_only=True)
    
    class Meta:
        model = ClassTradeRequest
        fields = ['id', 'owner', 'owner_student_id', 'offered_class', 'desired_class_number', 'desired_section_number', 'status', 'upvoted_by', 'downvoted_by', 'favorites', 'created_at']
