import random
import string
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login, Group
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (Department, Gender, Medicine, MedicineType, Receptionist, Staff, Prescription, 
                     Salary, Patient, Appointment, Specialization, Doctor, 
                     Schedule, TimeSlot, Token, Consultation, MedicalRecord, Bill)
from .validators import validate_mobile_number

# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    # validations
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
        fields = ['id', 'first_name', 'last_name', 'email', 'mobile_number', 'gender', 'dob', 
                  'joining_date', 'qualification', 'photo', 'department', 'group']
        extra_kwargs = {
            'email': {'required': True},
            'mobile_number': {'required': True},
            'dob': {'required': True},
            'gender': {'required': True},
            'qualification': {'required': True},
            'department': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'joining_date': {'required': True}
        }

    def validate_email(self, value):
        if Staff.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value

    def validate_group(self, value):
        try:
            group = Group.objects.get(id=value)
        except Group.DoesNotExist:
            raise serializers.ValidationError(f"Group with ID {value} does not exist.")
        return group
    
    def validate(self, data):
        # Call validators from validators.py
        validate_mobile_number(data.get('mobile_number'))
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
        print(password)
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

# Prescription
class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

# Salary
class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = '__all__'

# Medicine
class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['name', 'dose', 'type']

# Medicine Type
class MedicineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineType
        fields = '__all__'

# Receptionist
class ReceptionistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receptionist
        fields = '__all__'

# Staff
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

# Patient
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'full_name', 'dob', 'gender', 'mobile_number', 'address']

# Appointment
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

# Specialization
class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'specialization_name']

# Doctor
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'staff', 'specialization', 'consultation_fee', 'year_of_experience']

# Schedule
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'doctor', 'schedule_date', 'time_slot', 'token', 'status']

# Time Slot
class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'start_time', 'end_time']

# Token
class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['id', 'appointment', 'token_number', 'issued_at', 'status']

# Consultation
class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ['id', 'token', 'patient', 'symptoms', 'diagnosis', 'notes', 'additional_notes', 
                  'created_at', 'prescription', 'is_active']

# Medical Records
class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'doctors', 'record_date', 'consultation', 'updated_at']

# Bill
class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['id', 'appointment', 'total_amount', 'payment_status', 'created_at']

#gender

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'name']  # Include all the fields you want to expose

#dep
#Department
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name', 'base_salary']  # Include all the fields you want to expose