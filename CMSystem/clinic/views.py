
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer, SignupSerializer
from rest_framework.permissions import AllowAny

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

class MedicineViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]  # Authenticate using JWT
    permission_classes = [IsAuthenticated]  # Only allow authenticated users
    queryset = Medicine.objects.all()  # Fetch all medicines
    serializer_class = MedicineSerializer  # Use the MedicineSerializer


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
        
class ChangePasswordView(APIView):
    def post(self, request):
        staff_id = request.data.get('staff_id')  # Staff ID to identify the user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        # Fetch staff from the database
        try:
            staff = Staff.objects.get(id=staff_id)
        except Staff.DoesNotExist:
            return Response({"error": "Staff not found"}, status=status.HTTP_404_NOT_FOUND)

        # Validate old password
        if not check_password(old_password, staff.password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate new password
        if not new_password or len(new_password) < 8:
            return Response({"error": "New password must be at least 8 characters long"}, status=status.HTTP_400_BAD_REQUEST)

        # Set new password
        staff.set_password(new_password)
        staff.save()
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
    
class MedicineTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]  # Authenticate using JWT
    permission_classes = [IsAuthenticated]  # Only allow authenticated users
    queryset = MedicineType.objects.all()  # Fetch all medicine types
    serializer_class = MedicineTypeSerializer  # Use the MedicineTypeSerializer

class ReceptionistViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]  # Authenticate using JWT
    permission_classes = [IsAuthenticated]  # Only allow authenticated users
    queryset = Receptionist.objects.all()  # Fetch all receptionist records
    serializer_class = ReceptionistSerializer  # Use the ReceptionistSerializer