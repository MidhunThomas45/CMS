
from django.urls import path
from .views import LoginView, SignupView
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'prescriptions',views.PrescriptionViewSet)
router.register(r'salary',views.SalaryViewSet)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup')

]
urlpatterns+=router.urls
