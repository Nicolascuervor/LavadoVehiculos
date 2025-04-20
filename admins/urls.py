# admins/urls.py
from django.urls import path
from . import views

app_name = 'admins'

urlpatterns = [
    
    # URLs del Superpanel Administrativo
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/users/', views.admin_user_list, name='admin_user_list'),
    path('admin-panel/users/create/', views.admin_user_create, name='admin_user_create'),
    path('admin-panel/users/<int:pk>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('admin-panel/users/<int:pk>/delete/', views.admin_user_delete, name='admin_user_delete'),
    
    path('admin-panel/userprofiles/', views.admin_userprofile_list, name='admin_userprofile_list'),
    path('admin-panel/userprofiles/create/', views.admin_userprofile_create, name='admin_userprofile_create'),
    path('admin-panel/userprofiles/<int:pk>/edit/', views.admin_userprofile_edit, name='admin_userprofile_edit'),
    path('admin-panel/userprofiles/<int:pk>/delete/', views.admin_userprofile_delete, name='admin_userprofile_delete'),
    
    path('admin-panel/clientes/', views.admin_cliente_list, name='admin_cliente_list'),
    path('admin-panel/clientes/create/', views.admin_cliente_create, name='admin_cliente_create'),
    path('admin-panel/clientes/<int:pk>/edit/', views.admin_cliente_edit, name='admin_cliente_edit'),
    path('admin-panel/clientes/<int:pk>/delete/', views.admin_cliente_delete, name='admin_cliente_delete'),
    
    path('admin-panel/vehiculos/', views.admin_vehiculo_list, name='admin_vehiculo_list'),
    path('admin-panel/vehiculos/create/', views.admin_vehiculo_create, name='admin_vehiculo_create'),
    path('admin-panel/vehiculos/<int:pk>/edit/', views.admin_vehiculo_edit, name='admin_vehiculo_edit'),
    path('admin-panel/vehiculos/<int:pk>/delete/', views.admin_vehiculo_delete, name='admin_vehiculo_delete'),
    
    path('admin-panel/citas/', views.admin_cita_list, name='admin_cita_list'),
    path('admin-panel/citas/create/', views.admin_cita_create, name='admin_cita_create'),
    path('admin-panel/citas/<int:pk>/edit/', views.admin_cita_edit, name='admin_cita_edit'),
    path('admin-panel/citas/<int:pk>/delete/', views.admin_cita_delete, name='admin_cita_delete'),
    
    path('admin-panel/servicios/', views.admin_servicio_list, name='admin_servicio_list'),
    path('admin-panel/servicios/create/', views.admin_servicio_create, name='admin_servicio_create'),
    path('admin-panel/servicios/<int:pk>/edit/', views.admin_servicio_edit, name='admin_servicio_edit'),
    path('admin-panel/servicios/<int:pk>/delete/', views.admin_servicio_delete, name='admin_servicio_delete'),
    
    path('admin-panel/empleados/', views.admin_empleado_list, name='admin_empleado_list'),
    path('admin-panel/empleados/create/', views.admin_empleado_create, name='admin_empleado_create'),
    path('admin-panel/empleados/<int:pk>/edit/', views.admin_empleado_edit, name='admin_empleado_edit'),
    path('admin-panel/empleados/<int:pk>/delete/', views.admin_empleado_delete, name='admin_empleado_delete'),
    
    path('admin-panel/employee-requests/', views.admin_employee_request_list, name='admin_employee_request_list'),
    path('admin-panel/employee-requests/create/', views.admin_employee_request_create, name='admin_employee_request_create'),
    path('admin-panel/employee-requests/<int:pk>/edit/', views.admin_employee_request_edit, name='admin_employee_request_edit'),
    path('admin-panel/employee-requests/<int:pk>/delete/', views.admin_employee_request_delete, name='admin_employee_request_delete'),
    
    path('admin-panel/activity-logs/', views.admin_activity_log_list, name='admin_activity_log_list'),

    
    
]