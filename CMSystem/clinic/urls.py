
from django.urls import path, include
from .views import DoctorViewSet, LoginView, SignupView, PatientViewSet, AppointmentViewSet, SpecializationViewSet, StaffViewSet, ScheduleViewSet
from .views import TimeSlotViewSet, TokenViewSet, ConsultationViewSet, MedicalRecordViewSet, BillViewSet
from rest_framework.routers import DefaultRouter

#create a router object
router= DefaultRouter()

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

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('', include(router.urls)) #for adding api urls
]