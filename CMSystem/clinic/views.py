from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Prescription, Salary
from .serializers import LoginSerializer, SalarySerilaizer, SignupSerializer, PrescriptionSerializer
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
                "message": "Signup successful",
                "user": SignupSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Precription
class PrescriptionViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]  # Authenticate using JWT
    permission_classes = [IsAuthenticated]  # Only allow authenticated users
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

class SalaryViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]  # Authenticate using JWT
    permission_classes = [IsAuthenticated]  # Only allow authenticated users
    queryset = Salary.objects.all()
    serializer_class =SalarySerilaizer


