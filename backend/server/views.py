from rest_framework.decorators import api_view, authentication_classes, permission_classes # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.authentication import SessionAuthentication, TokenAuthentication # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from django.contrib.auth.models import User # type: ignore
from rest_framework.authtoken.models import Token # type: ignore
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404 # type: ignore

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