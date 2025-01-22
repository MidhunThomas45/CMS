from .import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView,
    SignupView,
    AddGroupView,
    ListGroupsView,
    DeleteGroupView,
    ChangePasswordView,
)

# Create a router object
router = DefaultRouter()

# Register viewsets with the router
router.register(r'staff', views.StaffViewSet)
router.register(r'patients', views.PatientViewSet)
router.register(r'appointments', views.AppointmentViewSet)
router.register(r'specializations', views.SpecializationViewSet)
router.register(r'doctors', views.DoctorViewSet)
router.register(r'schedules', views.ScheduleViewSet)
router.register(r'time-slots', views.TimeSlotViewSet)
router.register(r'tokens', views.TokenViewSet)
router.register(r'consultations', views.ConsultationViewSet)
router.register(r'medical-records', views.MedicalRecordViewSet)
router.register(r'bills', views.BillViewSet)
router.register(r'prescriptions', views.PrescriptionViewSet)
router.register(r'salary', views.SalaryViewSet)
router.register(r'medicines', views.MedicineViewSet, basename='medicine')
router.register(r'medicine-types', views.MedicineTypeViewSet)
router.register(r'receptionists', views.ReceptionistViewSet, basename='receptionist')
router.register(r'genders', views.GenderViewSet, basename='gender')
router.register(r'departments', views.DepartmentViewSet, basename='department')

# Define urlpatterns
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('api/', include(router.urls)),
    path('groups/add/', AddGroupView.as_view(), name='add-group'),
    path('groups/', ListGroupsView.as_view(), name='list-groups'),
    path('groups/delete/<int:group_id>/', DeleteGroupView.as_view(), name='delete-group'),
    path('staff/change-password/', ChangePasswordView.as_view(), name='staff-change-password'),
]

urlpatterns+=router.urls