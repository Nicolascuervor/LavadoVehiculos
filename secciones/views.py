# secciones/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.db.models import Q
from .models import (
    Cliente, Vehiculo, Empleado, Jornada, TurnoEmpleado, TipoInsumo, Insumo, Inventario,
    TipoLavado, Servicio, ConsumoInsumo, Factura, Cita, Promocion, CargaTrabajoEmpleado
)

# Función para verificar el rol del usuario
def role_required(role):
    def check_role(user):
        return hasattr(user, 'profile') and user.profile.role == role
    return user_passes_test(check_role, login_url='perfiles:dashboard')

# Vistas para Administrador
@login_required
@role_required('admin')
def cliente_admin_list(request):
    queryset = Cliente.objects.select_related('user').all()
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(nombre__icontains=search_query) |
            Q(apellido__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    paginator = Paginator(queryset, 10)  # 10 clientes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'clientes': page_obj,
        'search_query': search_query,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/cliente_admin_list.html', context)

@login_required
@role_required('admin')
def vehiculo_admin_list(request):
    queryset = Vehiculo.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'vehiculos': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/vehiculo_admin_list.html', context)

@login_required
@role_required('admin')
def empleado_admin_list(request):
    queryset = Empleado.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'empleados': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/empleado_admin_list.html', context)

@login_required
@role_required('admin')
def jornada_admin_list(request):
    queryset = Jornada.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'jornadas': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/jornada_admin_list.html', context)

@login_required
@role_required('admin')
def turno_admin_list(request):
    queryset = TurnoEmpleado.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'turnos': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/turno_admin_list.html', context)

@login_required
@role_required('admin')
def tipo_insumo_admin_list(request):
    queryset = TipoInsumo.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tipos_insumo': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/tipoinsumo_admin_list.html', context)

@login_required
@role_required('admin')
def insumo_admin_list(request):
    queryset = Insumo.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'insumos': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/insumo_admin_list.html', context)

@login_required
@role_required('admin')
def inventario_admin_list(request):
    queryset = Inventario.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'inventarios': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/inventario_admin_list.html', context)

@login_required
@role_required('admin')
@cache_page(60 * 15)  # Cachear por 15 minutos
def tipo_lavado_admin_list(request):
    queryset = TipoLavado.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tipos_lavado': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/tipolavado_admin_list.html', context)

@login_required
@role_required('admin')
def servicio_admin_list(request):
    queryset = Servicio.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'servicios': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/servicio_admin_list.html', context)

@login_required
@role_required('admin')
def consumo_insumo_admin_list(request):
    queryset = ConsumoInsumo.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'consumos': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/consumoinsumo_admin_list.html', context)

@login_required
@role_required('admin')
def factura_admin_list(request):
    queryset = Factura.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'facturas': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/factura_admin_list.html', context)

@login_required
@role_required('admin')
def cita_admin_list(request):
    queryset = Cita.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'citas': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/cita_admin_list.html', context)

@login_required
@role_required('admin')
@cache_page(60 * 15)  # Cachear por 15 minutos
def promocion_admin_list(request):
    queryset = Promocion.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'promociones': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/promocion_admin_list.html', context)

@login_required
@role_required('admin')
def carga_trabajo_admin_list(request):
    queryset = CargaTrabajoEmpleado.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'cargas': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/cargatrabajo_admin_list.html', context)

# Vistas para Lavador
@login_required
@role_required('lavador')
def servicio_lavador_list(request):
    queryset = Servicio.objects.filter(empleado__user=request.user).select_related('empleado', 'cliente')
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'servicios': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/servicio_lavador_list.html', context)

@login_required
@role_required('lavador')
def empleado_lavador_list(request):
    queryset = Empleado.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'empleados': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/empleado_lavador_list.html', context)

@login_required
@role_required('lavador')
def jornada_lavador_list(request):
    queryset = Jornada.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'jornadas': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/jornada_lavador_list.html', context)

@login_required
@role_required('lavador')
def turno_lavador_list(request):
    queryset = TurnoEmpleado.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'turnos': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/turno_lavador_list.html', context)

@login_required
@role_required('lavador')
def tipo_insumo_lavador_list(request):
    queryset = TipoInsumo.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tipos_insumo': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/tipoinsumo_lavador_list.html', context)

@login_required
@role_required('lavador')
def insumo_lavador_list(request):
    queryset = Insumo.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'insumos': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/insumo_lavador_list.html', context)

@login_required
@role_required('lavador')
def inventario_lavador_list(request):
    queryset = Inventario.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'inventarios': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/inventario_lavador_list.html', context)

@login_required
@role_required('lavador')
def tipo_lavado_lavador_list(request):
    queryset = TipoLavado.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tipos_lavado': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/tipolavado_lavador_list.html', context)

@login_required
@role_required('lavador')
def consumo_insumo_lavador_list(request):
    queryset = ConsumoInsumo.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'consumos': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/consumoinsumo_lavador_list.html', context)

@login_required
@role_required('lavador')
def factura_lavador_list(request):
    queryset = Factura.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'facturas': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/factura_lavador_list.html', context)

@login_required
@role_required('lavador')
def cita_lavador_list(request):
    queryset = Cita.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'citas': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/cita_lavador_list.html', context)

@login_required
@role_required('lavador')
@cache_page(60 * 15)
def promocion_lavador_list(request):
    queryset = Promocion.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'promociones': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/promocion_lavador_list.html', context)

@login_required
@role_required('lavador')
def carga_trabajo_lavador_list(request):
    queryset = CargaTrabajoEmpleado.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'cargas': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/cargatrabajo_lavador_list.html', context)

# Vistas para Recepcionista
@login_required
@role_required('recepcionista')
def servicio_recepcionista_list(request):
    queryset = Servicio.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'servicios': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/servicio_recepcionista_list.html', context)

@login_required
@role_required('recepcionista')
def cliente_recepcionista_list(request):
    queryset = Cliente.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'clientes': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/cliente_recepcionista_list.html', context)

@login_required
@role_required('recepcionista')
def vehiculo_recepcionista_list(request):
    queryset = Vehiculo.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'vehiculos': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/vehiculo_recepcionista_list.html', context)

@login_required
@role_required('recepcionista')
def factura_recepcionista_list(request):
    queryset = Factura.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'facturas': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/factura_recepcionista_list.html', context)

@login_required
@role_required('recepcionista')
def cita_recepcionista_list(request):
    queryset = Cita.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(cliente__nombre__icontains=search_query) |
            Q(cliente__apellido__icontains=search_query) |
            Q(vehiculo__placa__icontains=search_query)
        )

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'citas': page_obj,
        'search_query': search_query,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/cita_recepcionista_list.html', context)

@login_required
@role_required('recepcionista')
@cache_page(60 * 15)
def promocion_recepcionista_list(request):
    queryset = Promocion.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'promociones': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/promocion_recepcionista_list.html', context)

# Vistas para Supervisor
@login_required
@role_required('supervisor')
def empleado_supervisor_list(request):
    queryset = Empleado.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'empleados': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/empleado_supervisor_list.html', context)

@login_required
@role_required('supervisor')
def jornada_supervisor_list(request):
    queryset = Jornada.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'jornadas': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/jornada_supervisor_list.html', context)

@login_required
@role_required('supervisor')
def turno_supervisor_list(request):
    queryset = TurnoEmpleado.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'turnos': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/turno_supervisor_list.html', context)

@login_required
@role_required('supervisor')
def servicio_supervisor_list(request):
    queryset = Servicio.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'servicios': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/servicio_supervisor_list.html', context)

@login_required
@role_required('supervisor')
def carga_trabajo_supervisor_list(request):
    queryset = CargaTrabajoEmpleado.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'cargas': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/cargatrabajo_supervisor_list.html', context)

@login_required
@role_required('supervisor')
def consumo_insumo_supervisor_list(request):
    queryset = ConsumoInsumo.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'consumos': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/consumoinsumo_supervisor_list.html', context)

# Vistas para Cliente
@login_required
@role_required('cliente')
def cliente_self(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    context = {
        'cliente': cliente,
    }
    return render(request, 'secciones/cliente_self.html', context)

@login_required
@role_required('cliente')
def vehiculo_cliente_list(request):
    queryset = Vehiculo.objects.filter(cliente__user=request.user)
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'vehiculos': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/vehiculo_cliente_list.html', context)

@login_required
@role_required('cliente')
def cita_cliente_list(request):
    queryset = Cita.objects.filter(cliente__user=request.user)
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'citas': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/cita_cliente_list.html', context)

@login_required
@role_required('cliente')
def servicio_cliente_list(request):
    queryset = Servicio.objects.filter(cliente__user=request.user)
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'servicios': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/servicio_cliente_list.html', context)

@login_required
@role_required('cliente')
def factura_cliente_list(request):
    queryset = Factura.objects.filter(cliente__user=request.user)
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'facturas': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/factura_cliente_list.html', context)

@login_required
@role_required('cliente')
@cache_page(60 * 15)
def promocion_cliente_list(request):
    queryset = Promocion.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'promociones': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'secciones/promocion_cliente_list.html', context)