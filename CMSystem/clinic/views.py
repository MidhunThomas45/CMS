from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer, SignupSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets

# Login
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            tokens = serializer.save()
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Signup
class SignupView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to access this endpoint
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Staff Added Successfully",
                "user": SignupSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Staff
from .serializers import StaffSerializer
from .models import Staff
class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

# Patient
from .serializers import PatientSerializer
from .models import Patient
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        # Handle POST request and create the patient
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the patient data
            return Response({"message": "Patient added successfully!", "data": serializer.data}, 
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Appointment
from .serializers import AppointmentSerializer
from .models import Appointment
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

# Specialization
from .serializers import SpecializationSerializer
from .models import Specialization
class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

# Doctor
from .serializers import DoctorSerializer
from .models import Doctor
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

# Schedule
from .serializers import ScheduleSerializer
from .models import Schedule
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

# Time Slot
from .serializers import TimeSlotSerializer
from .models import TimeSlot
class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

# Token
from .serializers import TokenSerializer
from .models import Token
class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

# Consultation
from .serializers import ConsultationSerializer
from .models import Consultation
class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

# Medical record
from .serializers import MedicalRecordSerializer
from .models import MedicalRecord
class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

# Bill
from .serializers import BillSerializer
from .models import Bill
class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
