from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login, Group
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    Department, Gender, Medicine, MedicineType, Receptionist, Staff, Prescription,
    Salary, Patient, Appointment, Specialization, Doctor,
    Schedule, TimeSlot, Token, Consultation, MedicalRecord, Bill
)
from .validators import validate_mobile_number


# Login Serializer
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
        return user

    def save(self):
        user = self.validated_data
        refresh = RefreshToken.for_user(user)
        update_last_login(None, user)
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
        fields = [
            'id', 'first_name', 'last_name', 'email', 'mobile_number', 'gender', 'dob',
            'joining_date', 'qualification', 'photo', 'department', 'group'
        ]
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
        validate_mobile_number(data.get('mobile_number'))
        return data

    def generate_username(self, email, mobile_number):
        email_prefix = email.split('@')[0]
        mobile_suffix = mobile_number[-3:]
        return (email_prefix + mobile_suffix).lower()

    def generate_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choices(characters, k=8))

    def create(self, validated_data):
        group = validated_data.pop('group')
        email = validated_data['email']
        mobile_number = validated_data['mobile_number']

        username = self.generate_username(email, mobile_number)
        password = self.generate_password()

        staff = Staff.objects.create(username=username, **validated_data)
        staff.set_password(password)
        staff.save()

        group.user_set.add(staff)
        staff.generated_password = password
        return staff

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['username'] = instance.username
        rep['password'] = getattr(instance, 'generated_password', None)
        return rep






# Other serializers (unchanged except for imports)
class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'name']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name', 'base_salary']


class StaffSerializer(serializers.ModelSerializer):
    gender = GenderSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Staff
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'gender', 'qualification', 'photo', 'department']


class SalarySerializer(serializers.ModelSerializer):
    staff = StaffSerializer(read_only=True)

    class Meta:
        model = Salary
        fields = ['id', 'staff', 'base_salary', 'increment', 'deduction', 'net_salary', 'payment_status']


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'specialization_name']


class DoctorSerializer(serializers.ModelSerializer):
    # For GET: Include full details of related fields
    staff_details = StaffSerializer(source='staff', read_only=True)
    specialization_details = SpecializationSerializer(source='specialization', read_only=True)
    
    # For POST: Accept staff and specialization IDs
    staff = serializers.PrimaryKeyRelatedField(queryset=Staff.objects.all())
    specialization = serializers.PrimaryKeyRelatedField(queryset=Specialization.objects.all())

    class Meta:
        model = Doctor
        fields = [
            'id', 'staff', 'staff_details', 'specialization', 'specialization_details',
            'consultation_fee', 'year_of_experience'
        ]



class MedicineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineType
        fields = ['id', 'type_name']


class MedicineSerializer(serializers.ModelSerializer):
    type = MedicineTypeSerializer(read_only=True)

    class Meta:
        model = Medicine
        fields = ['id', 'name', 'dose', 'type']


class PatientSerializer(serializers.ModelSerializer):
    gender = GenderSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'full_name', 'dob', 'gender', 'mobile_number', 'address']


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'type', 'start_time', 'end_time']


class ScheduleSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    time_slot = TimeSlotSerializer(read_only=True, many=True)

    class Meta:
        model = Schedule
        fields = ['id', 'doctor', 'schedule_date', 'time_slot', 'token', 'status']


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    schedule = ScheduleSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'schedule', 'appointment_date']


class TokenSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer(read_only=True)

    class Meta:
        model = Token
        fields = ['id', 'appointment', 'token_number', 'issued_at', 'status']


class PrescriptionSerializer(serializers.ModelSerializer):
    # For GET: Include full details of related fields
    patient_details = PatientSerializer(source='patient', read_only=True)
    medicines_details = MedicineSerializer(source='medicines', many=True, read_only=True)
    
    # For POST: Accept IDs
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    medicines = serializers.PrimaryKeyRelatedField(many=True, queryset=Medicine.objects.all())

    class Meta:
        model = Prescription
        fields = [
            'id', 'patient', 'patient_details', 'medicines', 'medicines_details', 
            'dosage', 'frequency', 'duration'
        ]


class ConsultationSerializer(serializers.ModelSerializer):
    # For GET: Include full details of related fields
    tokens = TokenSerializer(source='token',read_only=True)
    prescriptions = PrescriptionSerializer(source='prescription',read_only=True)
    
    # For POST: Accept token and prescription IDs
    token = serializers.PrimaryKeyRelatedField(queryset=Token.objects.all())
    prescription = serializers.PrimaryKeyRelatedField(queryset=Prescription.objects.all())
    
    # For GET: Show full patient details
    patient_details = PatientSerializer(source='patient', read_only=True)

    class Meta:
        model = Consultation
        fields = [
            'id', 'token', 'prescription', 'patient', 'patient_details', 'symptoms', 
            'diagnosis', 'notes', 'additional_notes', 'created_at', 'is_active', 
            'tokens', 'prescriptions'
        ]


class MedicalRecordSerializer(serializers.ModelSerializer):
    # For GET: Include full details of related fields
    patient_details = PatientSerializer(source='patient', read_only=True)
    doctors_details = DoctorSerializer(source='doctors', many=True, read_only=True)
    consultation_details = ConsultationSerializer(source='consultation', read_only=True)
    
    # For POST: Accept IDs
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    doctors = serializers.PrimaryKeyRelatedField(many=True, queryset=Doctor.objects.all())
    consultation = serializers.PrimaryKeyRelatedField(queryset=Consultation.objects.all())

    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'patient', 'patient_details', 'doctors', 'doctors_details', 
            'record_date', 'consultation', 'consultation_details', 'updated_at'
        ]



class BillSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer(read_only=True)

    class Meta:
        model = Bill
        fields = ['id', 'appointment', 'total_amount', 'payment_status', 'created_at']


class ReceptionistSerializer(serializers.ModelSerializer):
    staff = StaffSerializer()

    class Meta:
        model = Receptionist
        fields = ['id', 'staff', 'created_at', 'updated_at']
