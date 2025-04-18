# admins/views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from perfiles.models import UserProfile, EmployeeRequest
from secciones.models import (
    Cliente, Vehiculo, Empleado, Jornada, TurnoEmpleado, TipoInsumo, Insumo,
    Inventario, TipoLavado, Servicio, ConsumoInsumo, Factura, Cita,
    Promocion, CargaTrabajoEmpleado
)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from datetime import date
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


def admin_required(view_func):
    def decorated_view(request, *args, **kwargs):
        # Lógica para verificar si el usuario es admin
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('login')  # O alguna otra página
        return view_func(request, *args, **kwargs)
    return decorated_view




def admin_dashboard(request):
    # Obtener la fecha actual
    today = date.today()

    # Total de Clientes Activos
    total_clientes = Cliente.objects.filter(estado='A').count() or 0

    # Servicios Hoy (servicios completados o en proceso hoy)
    servicios_hoy = Servicio.objects.filter(fecha=today).count()

    # Ingresos Hoy (suma de facturas pagadas hoy)
    ingresos_hoy = Factura.objects.filter(
        fecha_emision=today,
        estado='P'  # Pagada
    ).aggregate(Sum('total'))['total__sum'] or 0

    # Total de Empleados Activos
    total_empleados = Empleado.objects.filter(estado='A').count()

    context = {
        'total_clientes': total_clientes,
        'servicios_hoy': servicios_hoy,
        'ingresos_hoy': ingresos_hoy,
        'total_empleados': total_empleados,
    }
    return render(request, 'admins/dashboard.html', context)

# Dashboard
@admin_required
def dashboard(request):
    context = {
        'title': 'Panel de Administración',
    }
    return render(request, 'admins/dashboard.html', context)

# Gestión de Usuarios (User y UserProfile)
@admin_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'admins/user_list.html', {'users': users, 'title': 'Lista de Usuarios'})

@admin_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = user.profile if hasattr(user, 'profile') else None
    return render(request, 'admins/user_detail.html', {'user': user, 'profile': profile, 'title': f'Detalles de {user.username}'})

@admin_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'Usuario {user.username} eliminado con éxito.')
        return redirect('admins:user_list')
    return render(request, 'admins/user_confirm_delete.html', {'user': user, 'title': f'Eliminar {user.username}'})

# Gestión de Solicitudes de Empleados
@admin_required
def employee_request_list(request):
    requests = EmployeeRequest.objects.all()
    return render(request, 'admins/employee_request_list.html', {'requests': requests, 'title': 'Lista de Solicitudes de Empleados'})

@admin_required
def employee_request_detail(request, pk):
    employee_request = get_object_or_404(EmployeeRequest, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['approved', 'rejected']:
            employee_request.status = status
            employee_request.save()
            messages.success(request, f'Solicitud actualizada a {status}.')
            return redirect('admins:employee_request_list')
    return render(request, 'admins/employee_request_detail.html', {'employee_request': employee_request, 'title': f'Solicitud de {employee_request.user.username}'})

# Gestión de Clientes
@admin_required
def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'admins/cliente_list.html', {'clientes': clientes, 'title': 'Lista de Clientes'})


# Gestión de vehiculos
@admin_required
def vehiculo_list(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'admins/vehiculo_list.html', {'vehiculos': vehiculos, 'title': 'Lista de vehiculos'})



# Gestión de vehiculos
@admin_required
def service_list(request):
    services = Servicio.objects.all()
    return render(request, 'admins/servicio_list.html', {'servicios': services, 'title': 'Lista de vehiculos'})

def reports_dashboard(request):
    # Obtener la fecha actual
    today = date.today()

    # Total de Clientes Activos
    total_clientes = Cliente.objects.filter(estado='A').count() or 0

    # Servicios Hoy (servicios completados o en proceso hoy)
    servicios_hoy = Servicio.objects.filter(fecha=today).count()

    # Ingresos Hoy (suma de facturas pagadas hoy)
    ingresos_hoy = Factura.objects.filter(
        fecha_emision=today,
        estado='P'  # Pagada
    ).aggregate(Sum('total'))['total__sum'] or 0

    # Total de Empleados Activos
    total_empleados = Empleado.objects.filter(estado='A').count()

    context = {
        'total_clientes': total_clientes,
        'servicios_hoy': servicios_hoy,
        'ingresos_hoy': ingresos_hoy,
        'total_empleados': total_empleados,
    }
    return render(request, 'admins/reports_dashboard.html', context)


@admin_required
def cliente_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'admins/cliente_detail.html', {'cliente': cliente, 'title': f'Detalles de Cliente {cliente.id}'})

@admin_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado con éxito.')
        return redirect('admins:cliente_list')
    return render(request, 'admins/cliente_confirm_delete.html', {'cliente': cliente, 'title': f'Eliminar Cliente {cliente.id}'})

# Gestión de Vehículos
@admin_required
def vehiculo_list(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'admins/vehiculo_list.html', {'vehiculos': vehiculos, 'title': 'Lista de Vehículos'})

@admin_required
def vehiculo_detail(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    return render(request, 'admins/vehiculo_detail.html', {'vehiculo': vehiculo, 'title': f'Detalles de Vehículo {vehiculo.id}'})

@admin_required
def vehiculo_delete(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        vehiculo.delete()
        messages.success(request, 'Vehículo eliminado con éxito.')
        return redirect('admins:vehiculo_list')
    return render(request, 'admins/vehiculo_confirm_delete.html', {'vehiculo': vehiculo, 'title': f'Eliminar Vehículo {vehiculo.id}'})

# Gestión de Empleados
@admin_required
def empleado_list(request):
    empleados = Empleado.objects.all()
    return render(request, 'admins/empleado_list.html', {'empleados': empleados, 'title': 'Lista de Empleados'})

@admin_required
def empleado_detail(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    return render(request, 'admins/empleado_detail.html', {'empleado': empleado, 'title': f'Detalles de Empleado {empleado.id}'})

@admin_required
def empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        messages.success(request, 'Empleado eliminado con éxito.')
        return redirect('admins:empleado_list')
    return render(request, 'admins/empleado_confirm_delete.html', {'empleado': empleado, 'title': f'Eliminar Empleado {empleado.id}'})

# Gestión de Jornadas
@admin_required
def jornada_list(request):
    jornadas = Jornada.objects.all()
    return render(request, 'admins/jornada_list.html', {'jornadas': jornadas, 'title': 'Lista de Jornadas'})

@admin_required
def jornada_detail(request, pk):
    jornada = get_object_or_404(Jornada, pk=pk)
    return render(request, 'admins/jornada_detail.html', {'jornada': jornada, 'title': f'Detalles de Jornada {jornada.id}'})

@admin_required
def jornada_delete(request, pk):
    jornada = get_object_or_404(Jornada, pk=pk)
    if request.method == 'POST':
        jornada.delete()
        messages.success(request, 'Jornada eliminada con éxito.')
        return redirect('admins:jornada_list')
    return render(request, 'admins/jornada_confirm_delete.html', {'jornada': jornada, 'title': f'Eliminar Jornada {jornada.id}'})

# Gestión de Turnos
@admin_required
def turno_list(request):
    turnos = TurnoEmpleado.objects.all()
    return render(request, 'admins/turno_list.html', {'turnos': turnos, 'title': 'Lista de Turnos'})

@admin_required
def turno_detail(request, pk):
    turno = get_object_or_404(TurnoEmpleado, pk=pk)
    return render(request, 'admins/turno_detail.html', {'turno': turno, 'title': f'Detalles de Turno {turno.id}'})

@admin_required
def turno_delete(request, pk):
    turno = get_object_or_404(TurnoEmpleado, pk=pk)
    if request.method == 'POST':
        turno.delete()
        messages.success(request, 'Turno eliminado con éxito.')
        return redirect('admins:turno_list')
    return render(request, 'admins/turno_confirm_delete.html', {'turno': turno, 'title': f'Eliminar Turno {turno.id}'})

# Gestión de Tipos de Insumo
@admin_required
def tipo_insumo_list(request):
    tipos_insumo = TipoInsumo.objects.all()
    return render(request, 'admins/tipo_insumo_list.html', {'tipos_insumo': tipos_insumo, 'title': 'Lista de Tipos de Insumo'})

@admin_required
def tipo_insumo_detail(request, pk):
    tipo_insumo = get_object_or_404(TipoInsumo, pk=pk)
    return render(request, 'admins/tipo_insumo_detail.html', {'tipo_insumo': tipo_insumo, 'title': f'Detalles de Tipo de Insumo {tipo_insumo.id}'})

@admin_required
def tipo_insumo_delete(request, pk):
    tipo_insumo = get_object_or_404(TipoInsumo, pk=pk)
    if request.method == 'POST':
        tipo_insumo.delete()
        messages.success(request, 'Tipo de Insumo eliminado con éxito.')
        return redirect('admins:tipo_insumo_list')
    return render(request, 'admins/tipo_insumo_confirm_delete.html', {'tipo_insumo': tipo_insumo, 'title': f'Eliminar Tipo de Insumo {tipo_insumo.id}'})

# Gestión de Insumos
@admin_required
def insumo_list(request):
    insumos = Insumo.objects.all()
    return render(request, 'admins/insumo_list.html', {'insumos': insumos, 'title': 'Lista de Insumos'})

@admin_required
def insumo_detail(request, pk):
    insumo = get_object_or_404(Insumo, pk=pk)
    return render(request, 'admins/insumo_detail.html', {'insumo': insumo, 'title': f'Detalles de Insumo {insumo.id}'})

@admin_required
def insumo_delete(request, pk):
    insumo = get_object_or_404(Insumo, pk=pk)
    if request.method == 'POST':
        insumo.delete()
        messages.success(request, 'Insumo eliminado con éxito.')
        return redirect('admins:insumo_list')
    return render(request, 'admins/insumo_confirm_delete.html', {'insumo': insumo, 'title': f'Eliminar Insumo {insumo.id}'})

# Gestión de Inventarios
@admin_required
def inventario_list(request):
    inventarios = Inventario.objects.all()
    return render(request, 'admins/inventario_list.html', {'inventarios': inventarios, 'title': 'Lista de Inventarios'})

@admin_required
def inventario_detail(request, pk):
    inventario = get_object_or_404(Inventario, pk=pk)
    return render(request, 'admins/inventario_detail.html', {'inventario': inventario, 'title': f'Detalles de Inventario {inventario.id}'})

@admin_required
def inventario_delete(request, pk):
    inventario = get_object_or_404(Inventario, pk=pk)
    if request.method == 'POST':
        inventario.delete()
        messages.success(request, 'Inventario eliminado con éxito.')
        return redirect('admins:inventario_list')
    return render(request, 'admins/inventario_confirm_delete.html', {'inventario': inventario, 'title': f'Eliminar Inventario {inventario.id}'})

# Gestión de Tipos de Lavado
@admin_required
def tipo_lavado_list(request):
    tipos_lavado = TipoLavado.objects.all()
    return render(request, 'admins/tipo_lavado_list.html', {'tipos_lavado': tipos_lavado, 'title': 'Lista de Tipos de Lavado'})

@admin_required
def tipo_lavado_detail(request, pk):
    tipo_lavado = get_object_or_404(TipoLavado, pk=pk)
    return render(request, 'admins/tipo_lavado_detail.html', {'tipo_lavado': tipo_lavado, 'title': f'Detalles de Tipo de Lavado {tipo_lavado.id}'})

@admin_required
def tipo_lavado_delete(request, pk):
    tipo_lavado = get_object_or_404(TipoLavado, pk=pk)
    if request.method == 'POST':
        tipo_lavado.delete()
        messages.success(request, 'Tipo de Lavado eliminado con éxito.')
        return redirect('admins:tipo_lavado_list')
    return render(request, 'admins/tipo_lavado_confirm_delete.html', {'tipo_lavado': tipo_lavado, 'title': f'Eliminar Tipo de Lavado {tipo_lavado.id}'})

# Gestión de Servicios
@admin_required
def servicio_list(request):
    servicios = Servicio.objects.all()
    return render(request, 'admins/servicio_list.html', {'servicios': servicios, 'title': 'Lista de Servicios'})

@admin_required
def servicio_detail(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    return render(request, 'admins/servicio_detail.html', {'servicio': servicio, 'title': f'Detalles de Servicio {servicio.id}'})

@admin_required
def servicio_delete(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        servicio.delete()
        messages.success(request, 'Servicio eliminado con éxito.')
        return redirect('admins:servicio_list')
    return render(request, 'admins/servicio_confirm_delete.html', {'servicio': servicio, 'title': f'Eliminar Servicio {servicio.id}'})

# Gestión de Consumos de Insumo
@admin_required
def consumo_insumo_list(request):
    consumos = ConsumoInsumo.objects.all()
    return render(request, 'admins/consumo_insumo_list.html', {'consumos': consumos, 'title': 'Lista de Consumos de Insumo'})

@admin_required
def consumo_insumo_detail(request, pk):
    consumo = get_object_or_404(ConsumoInsumo, pk=pk)
    return render(request, 'admins/consumo_insumo_detail.html', {'consumo': consumo, 'title': f'Detalles de Consumo de Insumo {consumo.id}'})

@admin_required
def consumo_insumo_delete(request, pk):
    consumo = get_object_or_404(ConsumoInsumo, pk=pk)
    if request.method == 'POST':
        consumo.delete()
        messages.success(request, 'Consumo de Insumo eliminado con éxito.')
        return redirect('admins:consumo_insumo_list')
    return render(request, 'admins/consumo_insumo_confirm_delete.html', {'consumo': consumo, 'title': f'Eliminar Consumo de Insumo {consumo.id}'})

# Gestión de Facturas
@admin_required
def factura_list(request):
    facturas = Factura.objects.all()
    return render(request, 'admins/factura_list.html', {'facturas': facturas, 'title': 'Lista de Facturas'})

@admin_required
def factura_detail(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    return render(request, 'admins/factura_detail.html', {'factura': factura, 'title': f'Detalles de Factura {factura.id}'})

@admin_required
def factura_delete(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    if request.method == 'POST':
        factura.delete()
        messages.success(request, 'Factura eliminada con éxito.')
        return redirect('admins:factura_list')
    return render(request, 'admins/factura_confirm_delete.html', {'factura': factura, 'title': f'Eliminar Factura {factura.id}'})

# Gestión de Citas
@admin_required
def cita_list(request):
    citas = Cita.objects.all()
    return render(request, 'admins/cita_list.html', {'citas': citas, 'title': 'Lista de Citas'})

@admin_required
def cita_detail(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    return render(request, 'admins/cita_detail.html', {'cita': cita, 'title': f'Detalles de Cita {cita.id}'})

@admin_required
def cita_delete(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        cita.delete()
        messages.success(request, 'Cita eliminada con éxito.')
        return redirect('admins:cita_list')
    return render(request, 'admins/cita_confirm_delete.html', {'cita': cita, 'title': f'Eliminar Cita {cita.id}'})

# Gestión de Promociones
@admin_required
def promocion_list(request):
    promociones = Promocion.objects.all()
    return render(request, 'admins/promocion_list.html', {'promociones': promociones, 'title': 'Lista de Promociones'})

@admin_required
def promocion_detail(request, pk):
    promocion = get_object_or_404(Promocion, pk=pk)
    return render(request, 'admins/promocion_detail.html', {'promocion': promocion, 'title': f'Detalles de Promoción {promocion.id}'})

@admin_required
def promocion_delete(request, pk):
    promocion = get_object_or_404(Promocion, pk=pk)
    if request.method == 'POST':
        promocion.delete()
        messages.success(request, 'Promoción eliminada con éxito.')
        return redirect('admins:promocion_list')
    return render(request, 'admins/promocion_confirm_delete.html', {'promocion': promocion, 'title': f'Eliminar Promoción {promocion.id}'})

# Gestión de Carga de Trabajo
@admin_required
def carga_trabajo_list(request):
    cargas = CargaTrabajoEmpleado.objects.all()
    return render(request, 'admins/carga_trabajo_list.html', {'cargas': cargas, 'title': 'Lista de Cargas de Trabajo'})

@admin_required
def carga_trabajo_detail(request, pk):
    carga = get_object_or_404(CargaTrabajoEmpleado, pk=pk)
    return render(request, 'admins/carga_trabajo_detail.html', {'carga': carga, 'title': f'Detalles de Carga de Trabajo {carga.id}'})

@admin_required
def carga_trabajo_delete(request, pk):
    carga = get_object_or_404(CargaTrabajoEmpleado, pk=pk)
    if request.method == 'POST':
        carga.delete()
        messages.success(request, 'Carga de Trabajo eliminada con éxito.')
        return redirect('admins:carga_trabajo_list')
    return render(request, 'admins/carga_trabajo_confirm_delete.html', {'carga': carga, 'title': f'Eliminar Carga de Trabajo {carga.id}'})




@admin_required
def reports(request):
    from django.db.models import Sum, Count
    from datetime import timedelta
    from django.utils import timezone

    today = timezone.now().date()
    last_week = today - timedelta(days=7)

    # Ingresos por día (última semana)
    ingresos_por_dia = Factura.objects.filter(
        fecha_emision__gte=last_week,
        estado='P'
    ).values('fecha_emision').annotate(total=Sum('total')).order_by('fecha_emision')

    # Servicios por tipo de lavado
    servicios_por_tipo = Servicio.objects.values('tipo_lavado__nombre').annotate(total=Count('id'))

    context = {
        'title': 'Informes Administrativos',
        'ingresos_por_dia': ingresos_por_dia,
        'servicios_por_tipo': servicios_por_tipo,
    }
    return render(request, 'admins/reports.html', context)


class VehiculoListView(ListView):
    model = Vehiculo
    search_fields = ['placa', 'marca', 'modelo']

class VehiculoDetailView(DetailView):
    model = Vehiculo

class VehiculoCreateView(CreateView):
    model = Vehiculo
    fields = '__all__'

class VehiculoUpdateView(UpdateView):
    model = Vehiculo
    fields = '__all__'

class VehiculoDeleteView(DeleteView):
    model = Vehiculo