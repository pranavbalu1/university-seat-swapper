from rest_framework import serializers # type: ignore
from django.contrib.auth.models import User # type: ignore
from .models import StudentProfile, StudentClass, ClassTradeRequest, AcceptedRequest

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
    offered_class = StudentClassSerializer()
    requested_class = StudentClassSerializer()
    requester = UserSerializer()

    class Meta:
        model = ClassTradeRequest
        fields = ['id', 'requester', 'offered_class', 'requested_class', 'status', 'upvotes', 'downvotes', 'favorites']


class AcceptedRequestSerializer(serializers.ModelSerializer):
    request = ClassTradeRequestSerializer()
    accepted_by = UserSerializer()

    class Meta:
        model = AcceptedRequest
        fields = ['request', 'accepted_by']
