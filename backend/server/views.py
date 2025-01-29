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

from .serializers import UserSerializer, StudentProfileSerializer, StudentClassSerializer
from .models import StudentProfile, StudentClass
from .serializers import ClassTradeRequestSerializer
from .models import ClassTradeRequest



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

#Get Profile by User ID
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_profile_by_user_id(request, user_id):
    # Get the user by user_id or return 404
    user = get_object_or_404(User, id=user_id)
    
    # Get the user's profile or handle missing profile
    try:
        profile = user.profile  # Access via OneToOne relationship
    except StudentProfile.DoesNotExist:
        return Response({"detail": "Profile not found for this user."}, status=status.HTTP_404_NOT_FOUND)
    
    # Serialize and return the profile data
    serializer = StudentProfileSerializer(profile)
    return Response(serializer.data, status=status.HTTP_200_OK)

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

#Get Class Trade Requests
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_class_trade_requests(request):
    # Retrieve all class trade requests
    trade_requests = ClassTradeRequest.objects.all()
    serializer = ClassTradeRequestSerializer(trade_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Create Class Trade Request
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_class_trade_request(request):
    data = request.data
    user = request.user

    # Get the user's profile
    try:
        profile = StudentProfile.objects.get(user=user)
    except StudentProfile.DoesNotExist:
        return Response(
            {"detail": "Complete your profile before creating trade requests."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Get the offered class (validate ownership)
    offered_class = get_object_or_404(StudentClass, id=data['offered_class_id'], user=user)
    
    # Create the ClassTradeRequest with student_id from profile
    trade_request = ClassTradeRequest.objects.create(
        owner=user,
        owner_student_id=profile.student_id,  # Auto-populate from profile
        offered_class=offered_class,
        desired_class_number=data['desired_class_number'],
        desired_section_number=data['desired_section_number'],
    )

    serializer = ClassTradeRequestSerializer(trade_request)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


#Vote on a Class Trade Request
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vote_request(request, request_id):
    trade_request = get_object_or_404(ClassTradeRequest, id=request_id)
    user = request.user
    upvote = request.data.get('upvote', False)

    if upvote:
        if user in trade_request.downvoted_by.all():
            trade_request.downvoted_by.remove(user)
        if user not in trade_request.upvoted_by.all():
            trade_request.upvoted_by.add(user)
    else:
        if user in trade_request.upvoted_by.all():
            trade_request.upvoted_by.remove(user)
        if user not in trade_request.downvoted_by.all():
            trade_request.downvoted_by.add(user)

    #if upvote is null, remove the user from both upvoted_by and downvoted_by
    if upvote is None:
        if user in trade_request.upvoted_by.all():
            trade_request.upvoted_by.remove(user)
        if user in trade_request.downvoted_by.all():
            trade_request.downvoted_by.remove(user)

    serializer = ClassTradeRequestSerializer(trade_request)
    return Response(serializer.data, status=status.HTTP_200_OK)

#Toggle Favorite on a Request:
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, request_id):
    trade_request = get_object_or_404(ClassTradeRequest, id=request_id)
    user = request.user

    if user in trade_request.favorites.all():
        trade_request.favorites.remove(user)
    else:
        trade_request.favorites.add(user)

    serializer = ClassTradeRequestSerializer(trade_request)
    return Response(serializer.data, status=status.HTTP_200_OK)

#Delete a Class Exchange Request:
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_class_trade_request(request, request_id):
    trade_request = get_object_or_404(ClassTradeRequest, id=request_id)
    if trade_request.owner != request.user:
        return Response({"detail": "You do not have permission to delete this request."}, status=status.HTTP_403_FORBIDDEN)
    
    trade_request.delete()
    return Response({"detail": "Request deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

#Filter Class Exchange Requests:
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_class_trade_requests(request):
    filter_criteria = request.query_params
    requests = ClassTradeRequest.objects.all()

    if 'course_number' in filter_criteria:
        requests = requests.filter(desired_class_number=filter_criteria['course_number'])
    if 'class_name' in filter_criteria:
        requests = requests.filter(offered_class__class_name__icontains=filter_criteria['class_name'])
    if 'instructor' in filter_criteria:
        requests = requests.filter(offered_class__instructor__icontains=filter_criteria['instructor'])
    if 'status' in filter_criteria:
        requests = requests.filter(status=filter_criteria['status'])
    
    serializer = ClassTradeRequestSerializer(requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#Get Favorite Class Exchange Requests:
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_favorite_class_trade_requests(request):
    user = request.user
    # Retrieve all class trade requests that the user has favorited
    favorite_requests = ClassTradeRequest.objects.filter(favorites=user)
    serializer = ClassTradeRequestSerializer(favorite_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
