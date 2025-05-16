from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Profile
from .serializers import UserSerializer, ProfileSerializer, ProfileDetailSerializer, ProfileUpdateSerializer
from .permissions import IsOwnerOrReadOnly, IsOwner
# Create your views here.




User = get_user_model()


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user and automatically create an associated profile.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Create a profile for the user
        profile = Profile.objects.create(user=user)
        # Create auth token
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.id,
            'email': user.email,
            'token': token.key,
            'profile_id': profile.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileListView(generics.ListAPIView):
    """
    List all profiles (for authorized users only).
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]


class ProfileDetailView(generics.RetrieveAPIView):
    """
    Retrieve a profile (must be the owner or have read permissions).
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class ProfileUpdateView(generics.UpdateAPIView):
    """
    Update a profile (owner only).
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class ProfileDeleteView(generics.DestroyAPIView):
    """
    Delete a profile (owner only).
    """
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_destroy(self, instance):
        # Delete the user as well when profile is deleted
        user = instance.user
        instance.delete()
        user.delete()


class MyProfileView(APIView):
    """
    Get the current user's profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileDetailSerializer(profile)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_auth_token(request):
    """
    Get or create a token for the authenticated user.
    """
    token, created = Token.objects.get_or_create(user=request.user)
    return Response({'token': token.key})


