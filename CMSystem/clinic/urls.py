
from django.urls import path
from .views import LoginView, SignupView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('api/', include(router.urls)),
    path('groups/add/', AddGroupView.as_view(), name='add-group'),
    path('groups/', ListGroupsView.as_view(), name='list-groups'),
    path('groups/delete/<int:group_id>/', DeleteGroupView.as_view(), name='delete-group'),
    path('staff/change-password/', ChangePasswordView.as_view(), name='staff-change-password'),
]

