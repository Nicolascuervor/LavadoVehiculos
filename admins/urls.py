# admins/urls.py
from django.urls import path
from . import views

app_name = 'admins'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Usuarios
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    
    # Solicitudes de Empleados
    path('employee-requests/', views.employee_request_list, name='employee_request_list'),
    path('employee-requests/<int:pk>/', views.employee_request_detail, name='employee_request_detail'),
    
    # Clientes
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/<int:pk>/', views.cliente_detail, name='cliente_detail'),
    path('clientes/<int:pk>/delete/', views.cliente_delete, name='cliente_delete'),
    
    # Agrega más URLs para los otros modelos aquí...
    
    path('admins/', views.vehiculo_list, name='vehicle_list'),
    path('admins/', views.servicio_list, name='service_list'),
    path('admins/', views.reports_dashboard, name='reports_dashboard'),
    
    
    
]