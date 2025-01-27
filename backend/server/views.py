from django.utils import timezone # type: ignore
from rest_framework.decorators import api_view, authentication_classes, permission_classes # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.authentication import SessionAuthentication, TokenAuthentication # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from django.contrib.auth.models import User # type: ignore
from rest_framework.authtoken.models import Token # type: ignore
from django.shortcuts import get_object_or_404 # type: ignore
from django.contrib.auth.password_validation import validate_password # type: ignore
from django.db import IntegrityError # type: ignore

from .serializers import UserSerializer, StudentProfileSerializer, StudentClassSerializer, ClassTradeRequestSerializer, AcceptedRequestSerializer
from .models import StudentProfile, StudentClass, ClassTradeRequest, AcceptedRequest



# Login View
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    print(f"User {user.username} logged in with token: {token.key}")
    serializer = UserSerializer(instance=user)
    return Response({'token': token.key, 'user': serializer.data})

# Register View
@api_view(['POST'])
def register(request):
    data = request.data
    try:
        validate_password(data['password'])  # Validate password strength
    except Exception as e:
        return Response({"password": e.messages}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()  # This automatically saves the user
        user.set_password(request.data['password'])  # Hash the password
        user.save()

        token = Token.objects.create(user=user)
        print(f"User {user.username} logged in with token: {token.key}")
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

# Get the student profile
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    try:
        profile = user.profile  # Access the related StudentProfile
        serializer = StudentProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except StudentProfile.DoesNotExist:
        return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)


# Add a new class to a student's schedule
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_class(request):
    user = request.user
    data = request.data
    serializer = StudentClassSerializer(data=data)
    if serializer.is_valid():
        try:
            # Attempt to save the new class with the user association
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            # Handle the unique_together violation
            return Response(
                {"error": "You are already enrolled in this class."},
                status=status.HTTP_400_BAD_REQUEST
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Remove a class from a student's schedule
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_class(request):
    user = request.user
    data = request.data
    course_number = data.get('course_number')
    section_number = data.get('section_number')

    # Find the class the user is enrolled in
    try:
        student_class = StudentClass.objects.get(user=user, course_number=course_number, section_number=section_number)
        student_class.delete()  # Remove the class
        return Response({"detail": "Class removed successfully."}, status=status.HTTP_200_OK)
    except StudentClass.DoesNotExist:
        return Response({"detail": "Class not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_classes(request):
    user = request.user
    classes = StudentClass.objects.filter(user=user)
    serializer = StudentClassSerializer(classes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Create or update a class trade request
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_trade_request(request):
    data = request.data
    offered_class = get_object_or_404(StudentClass, id=data['offered_class_id'])
    requested_class = get_object_or_404(StudentClass, id=data['requested_class_id'])
    
    if offered_class.user == request.user:
        trade_request = ClassTradeRequest.objects.create(
            requester=request.user,
            offered_class=offered_class,
            requested_class=requested_class
        )
        serializer = ClassTradeRequestSerializer(trade_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({"detail": "You cannot offer your own class."}, status=status.HTTP_400_BAD_REQUEST)

# Upvote a trade request
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upvote_request(request, trade_request_id):
    trade_request = get_object_or_404(ClassTradeRequest, id=trade_request_id)

    if request.user in trade_request.favorites.all():
        return Response({"detail": "You already favorited this request."}, status=status.HTTP_400_BAD_REQUEST)

    trade_request.upvotes += 1
    trade_request.save()
    return Response(ClassTradeRequestSerializer(trade_request).data, status=status.HTTP_200_OK)

# Downvote a trade request
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def downvote_request(request, trade_request_id):
    trade_request = get_object_or_404(ClassTradeRequest, id=trade_request_id)

    trade_request.downvotes += 1
    trade_request.save()
    return Response(ClassTradeRequestSerializer(trade_request).data, status=status.HTTP_200_OK)

# Favorite a trade request
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def favorite_request(request, trade_request_id):
    trade_request = get_object_or_404(ClassTradeRequest, id=trade_request_id)

    if request.user in trade_request.favorites.all():
        return Response({"detail": "You already favorited this request."}, status=status.HTTP_400_BAD_REQUEST)

    trade_request.favorites.add(request.user)
    return Response(ClassTradeRequestSerializer(trade_request).data, status=status.HTTP_200_OK)

# Accept a trade request
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def accept_trade_request(request, trade_request_id):
    trade_request = get_object_or_404(ClassTradeRequest, id=trade_request_id)

    # Ensure the user meets the conditions for the request
    if trade_request.requester == request.user:
        return Response({"detail": "You cannot accept your own request."}, status=status.HTTP_400_BAD_REQUEST)

    accepted_request = AcceptedRequest.objects.create(request=trade_request, accepted_by=request.user)
    trade_request.status = 'accepted'
    trade_request.save()

    return Response(AcceptedRequestSerializer(accepted_request).data, status=status.HTTP_200_OK)

# Get all trade requests
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_trade_requests(request):
    trade_requests = ClassTradeRequest.objects.filter(status='open')
    serializer = ClassTradeRequestSerializer(trade_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Remove a trade request created by the current user
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_trade_request(request, trade_request_id):
    try:
        trade_request = ClassTradeRequest.objects.get(id=trade_request_id, requester=request.user)
        trade_request.delete()
        return Response({"detail": "Trade request deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except ClassTradeRequest.DoesNotExist:
        return Response({"detail": "Request not found or you do not have permission to delete this request."}, status=status.HTTP_404_NOT_FOUND)


# Mark a trade request as accepted by the user who created it (self-acceptance)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def mark_request_accepted(request, trade_request_id):
    try:
        trade_request = ClassTradeRequest.objects.get(id=trade_request_id, requester=request.user)

        # Mark as accepted if the request is open
        if trade_request.status == 'open':
            trade_request.status = 'accepted'
            trade_request.save()

            # Create AcceptedRequest record
            AcceptedRequest.objects.create(request=trade_request, accepted_by=request.user)

            return Response(ClassTradeRequestSerializer(trade_request).data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Request has already been accepted or closed."}, status=status.HTTP_400_BAD_REQUEST)
    except ClassTradeRequest.DoesNotExist:
        return Response({"detail": "Request not found or you do not have permission to accept this request."}, status=status.HTTP_404_NOT_FOUND)
