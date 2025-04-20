# perfiles/urls.py
from django.urls import path
from .views import (
    register, profile, dashboard,
    UserProfileView, EmployeeRequestCreateView,
    EmployeeRequestListView, EmployeeRequestDetailView,
)

app_name = 'perfiles'

urlpatterns = [
    path('', dashboard, name='dashboard'),  # Ruta raíz
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    

    
    # URLs de API (manteniendo las CBVs para Django REST Framework)
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/employee-request/create/', EmployeeRequestCreateView.as_view(), name='employee-request-create'),
    path('api/employee-requests/', EmployeeRequestListView.as_view(), name='employee-request-list'),
    path('api/employee-requests/<int:pk>/', EmployeeRequestDetailView.as_view(), name='employee-request-detail'),
]