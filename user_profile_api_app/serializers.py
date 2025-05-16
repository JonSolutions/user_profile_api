from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Profile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the custom User model."""

    password = serializers.CharField( required=True, validators=[validate_password])
    password2 = serializers.CharField( required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model."""

    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'email', 'first_name', 'last_name', 'bio', 'birth_date',
                  'profile_picture', 'location', 'website', 'phone_number',
                  'created_at', 'updated_at')


class ProfileDetailSerializer(ProfileSerializer):
    """Detailed Profile serializer with full user information."""

    class Meta(ProfileSerializer.Meta):
        fields = ProfileSerializer.Meta.fields


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profiles."""

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'birth_date',
                  'profile_picture', 'location', 'website', 'phone_number')