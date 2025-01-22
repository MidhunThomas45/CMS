from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import check_password

from .models import (
    MedicineType, Prescription, Receptionist, Salary, Medicine, Staff, 
    Patient, Appointment, Specialization, Doctor, Schedule, TimeSlot, 
    Token, Consultation, MedicalRecord, Bill
)
from .serializers import (
    LoginSerializer, SignupSerializer, StaffSerializer, PatientSerializer, 
    AppointmentSerializer, SpecializationSerializer, DoctorSerializer, 
    ScheduleSerializer, TimeSlotSerializer, TokenSerializer, 
    ConsultationSerializer, MedicalRecordSerializer, BillSerializer, 
    PrescriptionSerializer, MedicineSerializer, SalarySerilaizer, 
    MedicineTypeSerializer, ReceptionistSerializer
)

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
class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [AllowAny]


# Patient
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Patient added successfully!", "data": serializer.data}, 
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Appointment
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny]


# Specialization
class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [AllowAny]


# Doctor
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


# Schedule
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [AllowAny]


# Time Slot
class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [AllowAny]


# Token
class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    permission_classes = [AllowAny]


# Consultation
class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [AllowAny]


# Medical Record
class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [AllowAny]


# Bill
class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [AllowAny]


# Prescription
class PrescriptionViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


# Salary
class SalaryViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Salary.objects.all()
    serializer_class = SalarySerilaizer


# Group Management
class AddGroupView(APIView):
    def post(self, request):
        group_name = request.data.get('group_name')
        if not group_name:
            return Response({"error": "Group name is required"}, status=status.HTTP_400_BAD_REQUEST)

        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            return Response({"message": f"Group '{group_name}' created successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"message": f"Group '{group_name}' already exists."}, status=status.HTTP_200_OK)


class ListGroupsView(APIView):
    def get(self, request):
        groups = Group.objects.all().values('id', 'name')
        return Response({"groups": list(groups)}, status=status.HTTP_200_OK)


class DeleteGroupView(APIView):
    def delete(self, request, group_id):
        try:
            group = Group.objects.get(id=group_id)
            group.delete()
            return Response({"message": f"Group '{group.name}' deleted successfully!"}, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)


# Change Password
class ChangePasswordView(APIView):
    def post(self, request):
        staff_id = request.data.get('staff_id')
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        try:
            staff = Staff.objects.get(id=staff_id)
        except Staff.DoesNotExist:
            return Response({"error": "Staff not found"}, status=status.HTTP_404_NOT_FOUND)

        if not check_password(old_password, staff.password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        if not new_password or len(new_password) < 8:
            return Response({"error": "New password must be at least 8 characters long"}, status=status.HTTP_400_BAD_REQUEST)

        staff.set_password(new_password)
        staff.save()
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)


# Medicine Type
class MedicineTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = MedicineType.objects.all()
    serializer_class = MedicineTypeSerializer


# Receptionist
class ReceptionistViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Receptionist.objects.all()
    serializer_class = ReceptionistSerializer


# Medicine
class MedicineViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
