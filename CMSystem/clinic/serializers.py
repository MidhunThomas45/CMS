from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed("Invalid username or password.")
        
        if not user.is_active:
            raise AuthenticationFailed("This account is deactivated.")
        
        # If authentication passes, return the user
        return user

    def save(self):
        user = self.validated_data
        refresh = RefreshToken.for_user(user)  # Generate JWT tokens
        update_last_login(None, user)  # Optional: Update the last login timestamp
        
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "username": user.username,
                "email": user.email,
            }
        }