from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DoctorViewSet,
    LoginView,
    SignupView,
    PatientViewSet,
    AppointmentViewSet,
    SpecializationViewSet,
    StaffViewSet,
    ScheduleViewSet,
    TimeSlotViewSet,
    TokenViewSet,
    ConsultationViewSet,
    MedicalRecordViewSet,
    BillViewSet,
    PrescriptionViewSet,
    SalaryViewSet,
    MedicineViewSet,
    MedicineTypeViewSet,
    ReceptionistViewSet,
    AddGroupView,
    ListGroupsView,
    DeleteGroupView,
    ChangePasswordView,
)

# Create a router object
router = DefaultRouter()

# Register viewsets with the router
router.register(r'staff', StaffViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'specializations', SpecializationViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'time-slots', TimeSlotViewSet)
router.register(r'tokens', TokenViewSet)
router.register(r'consultations', ConsultationViewSet)
router.register(r'medical-records', MedicalRecordViewSet)
router.register(r'bills', BillViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'salary', SalaryViewSet)
router.register(r'medicines', MedicineViewSet, basename='medicine')
router.register(r'medicine-types', MedicineTypeViewSet)
router.register(r'receptionists', ReceptionistViewSet, basename='receptionist')

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