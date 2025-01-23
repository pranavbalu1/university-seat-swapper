from rest_framework.decorators import api_view, authentication_classes, permission_classes # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.authentication import SessionAuthentication, TokenAuthentication # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from django.contrib.auth.models import User # type: ignore
from rest_framework.authtoken.models import Token # type: ignore
from django.shortcuts import get_object_or_404 # type: ignore

from .serializers import UserSerializer, StudentProfileSerializer, StudentClassSerializer
from .models import StudentProfile, StudentClass

# Login View
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({'token': token.key, 'user': serializer.data})

# Register View
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()  # This automatically saves the user
        user.set_password(request.data['password'])  # Hash the password
        user.save()

        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Test Token View
@api_view(['GET'])
@authentication_classes([TokenAuthentication])  # Ensure TokenAuthentication is used
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response(f"Token validation successful for {request.user.username}", status=status.HTTP_200_OK)


# Create or update student profile
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_or_update_profile(request):
    user = request.user
    data = request.data
    profile, created = StudentProfile.objects.get_or_create(user=user)

    # Update or create profile data
    profile.student_id = data.get('student_id', profile.student_id)
    profile.full_name = data.get('full_name', profile.full_name)
    profile.email = data.get('email', profile.email)
    profile.save()

    serializer = StudentProfileSerializer(profile)
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


# Add a new class to a student's schedule
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_class(request):
    user = request.user
    data = request.data
    serializer = StudentClassSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=user)  # Associate the class with the logged-in user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

