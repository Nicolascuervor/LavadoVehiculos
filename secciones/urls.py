# secciones/urls.py
from django.urls import path, include
from . import views

app_name = 'secciones'

# URLs para Administrador
admin_patterns = [
    path('admin/clientes/', views.cliente_admin_list, name='cliente-admin-list'),
    path('admin/vehiculos/', views.vehiculo_admin_list, name='vehiculo-admin-list'),
    path('admin/empleados/', views.empleado_admin_list, name='empleado-admin-list'),
    path('admin/jornadas/', views.jornada_admin_list, name='jornada-admin-list'),
    path('admin/turnos/', views.turno_admin_list, name='turno-admin-list'),
    path('admin/tipos-insumo/', views.tipo_insumo_admin_list, name='tipoinsumo-admin-list'),
    path('admin/insumos/', views.insumo_admin_list, name='insumo-admin-list'),
    path('admin/inventarios/', views.inventario_admin_list, name='inventario-admin-list'),
    path('admin/tipos-lavado/', views.tipo_lavado_admin_list, name='tipolavado-admin-list'),
    path('admin/servicios/', views.servicio_admin_list, name='servicio-admin-list'),
    path('admin/consumos-insumo/', views.consumo_insumo_admin_list, name='consumoinsumo-admin-list'),
    path('admin/facturas/', views.factura_admin_list, name='factura-admin-list'),
    path('admin/citas/', views.cita_admin_list, name='cita-admin-list'),
    path('admin/promociones/', views.promocion_admin_list, name='promocion-admin-list'),
    path('admin/carga-trabajo/', views.carga_trabajo_admin_list, name='cargatrabajo-admin-list'),
]

# URLs para Lavador
lavador_patterns = [
    path('lavador/servicios/', views.servicio_lavador_list, name='servicio-lavador-list'),
    path('lavador/empleados/', views.empleado_lavador_list, name='empleado-lavador-list'),
    path('lavador/jornadas/', views.jornada_lavador_list, name='jornada-lavador-list'),
    path('lavador/turnos/', views.turno_lavador_list, name='turno-lavador-list'),
    path('lavador/tipos-insumo/', views.tipo_insumo_lavador_list, name='tipoinsumo-lavador-list'),
    path('lavador/insumos/', views.insumo_lavador_list, name='insumo-lavador-list'),
    path('lavador/inventarios/', views.inventario_lavador_list, name='inventario-lavador-list'),
    path('lavador/tipos-lavado/', views.tipo_lavado_lavador_list, name='tipolavado-lavador-list'),
    path('lavador/consumos-insumo/', views.consumo_insumo_lavador_list, name='consumoinsumo-lavador-list'),
    path('lavador/facturas/', views.factura_lavador_list, name='factura-lavador-list'),
    path('lavador/citas/', views.cita_lavador_list, name='cita-lavador-list'),
    path('lavador/promociones/', views.promocion_lavador_list, name='promocion-lavador-list'),
    path('lavador/carga-trabajo/', views.carga_trabajo_lavador_list, name='cargatrabajo-lavador-list'),
]

# URLs para Recepcionista
recepcionista_patterns = [
    path('recepcionista/servicios/', views.servicio_recepcionista_list, name='servicio-recepcionista-list'),
    path('recepcionista/clientes/', views.cliente_recepcionista_list, name='cliente-recepcionista-list'),
    path('recepcionista/vehiculos/', views.vehiculo_recepcionista_list, name='vehiculo-recepcionista-list'),
    path('recepcionista/facturas/', views.factura_recepcionista_list, name='factura-recepcionista-list'),
    path('recepcionista/citas/', views.cita_recepcionista_list, name='cita-recepcionista-list'),
    path('recepcionista/promociones/', views.promocion_recepcionista_list, name='promocion-recepcionista-list'),
]

# URLs para Supervisor
supervisor_patterns = [
    path('supervisor/empleados/', views.empleado_supervisor_list, name='empleado-supervisor-list'),
    path('supervisor/jornadas/', views.jornada_supervisor_list, name='jornada-supervisor-list'),
    path('supervisor/turnos/', views.turno_supervisor_list, name='turno-supervisor-list'),
    path('supervisor/servicios/', views.servicio_supervisor_list, name='servicio-supervisor-list'),
    path('supervisor/carga-trabajo/', views.carga_trabajo_supervisor_list, name='cargatrabajo-supervisor-list'),
    path('supervisor/consumos-insumo/', views.consumo_insumo_supervisor_list, name='consumoinsumo-supervisor-list'),
]

# URLs para Cliente
cliente_patterns = [
    path('cliente/perfil/', views.cliente_self, name='cliente-self'),
    path('cliente/vehiculos/', views.vehiculo_cliente_list, name='vehiculo-cliente-list'),
    path('cliente/citas/', views.cita_cliente_list, name='cita-cliente-list'),
    path('cliente/servicios/', views.servicio_cliente_list, name='servicio-cliente-list'),
    path('cliente/facturas/', views.factura_cliente_list, name='factura-cliente-list'),
    path('cliente/promociones/', views.promocion_cliente_list, name='promocion-cliente-list'),
]

# Combinar todas las URLs
urlpatterns = [
    path('', include(admin_patterns)),
    path('', include(lavador_patterns)),
    path('', include(recepcionista_patterns)),
    path('', include(supervisor_patterns)),
    path('', include(cliente_patterns)),
]