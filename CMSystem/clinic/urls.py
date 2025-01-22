
from django.urls import include, path
from django.views import View
from .import views
from .views import AddGroupView, ChangePasswordView, DeleteGroupView, ListGroupsView, LoginView, MedicineTypeViewSet, MedicineViewSet, ReceptionistViewSet, SignupView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'medicines', MedicineViewSet, basename='medicine')
router.register(r'medicine-types',views.MedicineTypeViewSet)
router.register(r'receptionists', ReceptionistViewSet, basename='receptionist')

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