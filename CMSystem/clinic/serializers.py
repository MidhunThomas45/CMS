import random
import string
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
from .models import Staff
from .validators import validate_mobile_number, validate_dob, validate_joining_date


# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    #validations
    def validate_mobile_number(self, value):
        validate_mobile_number(value)
        return value

    def validate_dob(self, value):
        validate_dob(value)
        return value

    def validate_joining_date(self, value):
        validate_joining_date(value)
        return value

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

# Signup Serializer
class SignupSerializer(serializers.ModelSerializer):
    group = serializers.IntegerField(write_only=True)
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'email', 'mobile_number', 'gender', 'dob', 
                  'joining_date', 'qualification', 'photo', 'department', 'group']
        extra_kwargs = {
            'email': {'required': True},
            'mobile_number': {'required': True},
            'dob': {'required': True},
            'gender': {'required': True},
            'qualification': {'required': True},
            'department': {'required': True},
            'first_name': { 'required': True},
            'last_name': { 'required': True}
        }

    def validate_group(self, value):
        try:
            group = Group.objects.get(id=value)
        except Group.DoesNotExist:
            raise serializers.ValidationError(f"Group with ID {value} does not exist.")
        return group
    
    def validate(self, data):
        """Object-level validation."""
        # Call validators from validators.py
        validate_mobile_number(data.get('mobile_number'))
        validate_dob(data.get('dob'))
        validate_joining_date(data.get('joining_date'))
        return data
    
    def generate_username(self, email, mobile_number):
        # Extract the part of the email before '@'
        email_prefix = email.split('@')[0]
        # Get the last three digits of the mobile number
        mobile_suffix = mobile_number[-3:]
        return (email_prefix + mobile_suffix).lower()
    
    def generate_password(self):
        # Generate a random password with letters, digits, and symbols
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choices(characters, k=8))
    
    def create(self, validated_data):
        group = validated_data.pop('group')  # Get the group object
        email = validated_data['email']
        mobile_number = validated_data['mobile_number']

        # Generate username and password
        username = self.generate_username(email, mobile_number)
        password = self.generate_password()

        # Create the staff user
        staff = Staff.objects.create(username=username, **validated_data)
        staff.set_password(password)
        staff.save()
        
        # Assign the user to the group
        group.user_set.add(staff)
        # Return the generated username and password
        staff.generated_password = password  # Attach it temporarily to return it in response
        return staff
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['username'] = instance.username
        rep['password'] = getattr(instance, 'generated_password', None)  # Add generated password to response
        return rep 
