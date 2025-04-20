# perfiles/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from functools import wraps
from .forms import (
    UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ClienteUpdateForm,
    AdminUserForm, AdminUserUpdateForm, AdminUserProfileForm, AdminClienteForm,
    AdminVehiculoForm, AdminCitaForm, AdminServicioForm, AdminEmpleadoForm,
    AdminEmployeeRequestForm
)
from perfiles.models import UserProfile, EmployeeRequest, ActivityLog
from secciones.models import Cita, Servicio, Vehiculo, Cliente, Empleado
from secciones.forms import VehiculoForm

# Decorador para restringir acceso a administradores
def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        try:
            user_profile = request.user.profile
            if user_profile.role != 'admin':
                messages.error(request, 'No tienes permiso para acceder a esta sección.')
                return redirect('perfiles:dashboard')
        except UserProfile.DoesNotExist:
            messages.error(request, 'No tienes un perfil asociado. Contacta al administrador.')
            return redirect('perfiles:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

# Vistas existentes (mantenidas como están, con ajustes menores)
def custom_404(request, exception):
    return render(request, 'perfiles/404.html', status=404)

def custom_500(request):
    return render(request, 'perfiles/500.html', status=500)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("Usuario creado:", user.username)
            try:
                user_profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={'role': 'cliente'}
                )
                print("UserProfile creado o recuperado:", user_profile)
                if Cliente.objects.filter(identificacion=form.cleaned_data['identification']).exists():
                    messages.error(request, 'El identificador ya está en uso.')
                    print("Error: Identificador ya en uso:", form.cleaned_data['identification'])
                    return render(request, 'perfiles/register.html', {'form': form})
                cliente = Cliente.objects.create(
                    usuario=user,
                    nombre=form.cleaned_data['first_name'] or 'Nombre',
                    apellido=form.cleaned_data['last_name'] or 'Apellido',
                    email=form.cleaned_data['email'],
                    identificacion=form.cleaned_data['identification'],
                    telefono=form.cleaned_data['telefono'],
                )
                print("Cliente creado manualmente:", cliente)
                login(request, user)
                messages.success(request, '¡Tu cuenta ha sido creada! Ahora puedes iniciar sesión.')
                return redirect('perfiles:dashboard')
            except Exception as e:
                print("Error al crear UserProfile o Cliente:", str(e))
                messages.error(request, f'Error al registrar: {str(e)}')
                return render(request, 'perfiles/register.html', {'form': form})
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegisterForm()
    return render(request, 'perfiles/register.html', {'form': form})

@login_required
def profile(request):
    try:
        cliente = Cliente.objects.get(usuario=request.user)
    except Cliente.DoesNotExist:
        messages.error(request, 'No tienes un cliente asociado. Contacta al administrador.')
        return redirect('perfiles:dashboard')

    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, role='cliente')
        if not Cliente.objects.filter(usuario=request.user).exists():
            Cliente.objects.create(
                usuario=request.user,
                nombre=request.user.first_name or 'Nombre',
                apellido=request.user.last_name or 'Apellido',
                email=request.user.email,
                identificacion=request.user.username,
                telefono='',
            )

    vehiculos = Vehiculo.objects.filter(usuario=request.user, cliente=cliente, estado='A')
    vehiculo_form = VehiculoForm()
    MAX_VEHICULOS = 10
    puede_agregar = len(vehiculos) < MAX_VEHICULOS

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        photo_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        cliente_form = ClienteUpdateForm(request.POST, instance=cliente)

        if 'action' in request.POST:
            action = request.POST.get('action')
            vehiculo_id = request.POST.get('vehiculo_id')

            if action == 'create' and puede_agregar:
                vehiculo_form = VehiculoForm(request.POST)
                if vehiculo_form.is_valid():
                    vehiculo = vehiculo_form.save(commit=False)
                    vehiculo.usuario = request.user
                    vehiculo.cliente = cliente
                    vehiculo.estado = 'A'
                    vehiculo.save()
                    messages.success(request, 'Vehículo registrado con éxito.')
                    return redirect('perfiles:profile')

            elif action == 'update' and vehiculo_id:
                vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id, usuario=request.user, cliente=cliente)
                vehiculo_form = VehiculoForm(request.POST, instance=vehiculo)
                if vehiculo_form.is_valid():
                    vehiculo_form.save()
                    messages.success(request, 'Vehículo actualizado con éxito.')
                    return redirect('perfiles:profile')

            elif action == 'delete' and vehiculo_id:
                vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id, usuario=request.user, cliente=cliente)
                vehiculo.estado = 'I'
                vehiculo.save()
                messages.success(request, 'Vehículo marcado como inactivo.')
                return redirect('perfiles:profile')

        if user_form.is_valid() and photo_form.is_valid() and cliente_form.is_valid():
            user_form.save()
            photo_form.save()
            cliente_form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado con éxito!')
            return redirect('perfiles:profile')
        else:
            messages.error(request, 'Error al actualizar el perfil. Por favor, revisa los campos.')
    
    else:
        user_form = UserUpdateForm(instance=request.user)
        photo_form = ProfileUpdateForm(instance=user_profile)
        cliente_form = ClienteUpdateForm(instance=cliente)

    context = {
        'user_form': user_form,
        'photo_form': photo_form,
        'cliente_form': cliente_form,
        'vehiculos': vehiculos,
        'vehiculo_form': vehiculo_form,
        'puede_agregar': puede_agregar,
    }
    return render(request, 'perfiles/profile.html', context)

@login_required
def dashboard(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user, role='cliente')
        if not Cliente.objects.filter(usuario=request.user).exists():
            Cliente.objects.create(
                usuario=request.user,
                nombre=request.user.first_name or 'Nombre',
                apellido=request.user.last_name or 'Apellido',
                email=request.user.email,
                identificacion=request.user.username,
                telefono='',
            )

    citas_pendientes = 0
    servicios_completados = 0
    vehiculos_atendidos = 0

    if user_profile.role == 'cliente':
        try:
            cliente = Cliente.objects.get(usuario=request.user)
            citas_pendientes = Cita.objects.filter(cliente=cliente, estado='pendiente').count()
            servicios_completados = Servicio.objects.filter(cita__cliente=cliente, estado='completado').count()
            vehiculos_atendidos = Vehiculo.objects.filter(usuario=request.user, estado='A').count()
        except Cliente.DoesNotExist:
            messages.warning(request, 'No tienes un cliente asociado. Contacta al administrador.')
            citas_pendientes = 0
            servicios_completados = 0
            vehiculos_atendidos = 0
    elif user_profile.role == 'admin':
        citas_pendientes = Cita.objects.filter(estado='pendiente').count()
        servicios_completados = Servicio.objects.filter(estado='completado').count()
        vehiculos_atendidos = Vehiculo.objects.filter(estado='A').count()
    else:
        citas_pendientes = Cita.objects.filter(estado='pendiente').count()
        servicios_completados = Servicio.objects.filter(estado='completado').count()
        vehiculos_atendidos = Vehiculo.objects.filter(estado='A').count()

    context = {
        'user': request.user,
        'citas_pendientes': citas_pendientes,
        'servicios_completados': servicios_completados,
        'vehiculos_atendidos': vehiculos_atendidos,
    }
    return render(request, 'perfiles/dashboard.html', context)

# Nuevas vistas para el Superpanel Administrativo
@admin_required
def admin_panel(request):
    # Estadísticas para el dashboard
    total_users = User.objects.count()
    total_clientes = Cliente.objects.count()
    total_vehiculos = Vehiculo.objects.count()
    total_citas = Cita.objects.count()
    total_servicios = Servicio.objects.count()
    total_empleados = Empleado.objects.count()
    recent_activities = ActivityLog.objects.order_by('-timestamp')[:10]

    context = {
        'total_users': total_users,
        'total_clientes': total_clientes,
        'total_vehiculos': total_vehiculos,
        'total_citas': total_citas,
        'total_servicios': total_servicios,
        'total_empleados': total_empleados,
        'recent_activities': recent_activities,
    }
    return render(request, 'admins/admin_panel.html', context)

# CRUD para User
@admin_required
def admin_user_list(request):
    users = User.objects.all()
    return render(request, 'admins/admin_user_list.html', {'users': users})

@admin_required
def admin_user_create(request):
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Usuario creado con éxito.')
            return redirect('admins:admin_user_list')
    else:
        form = AdminUserForm()
    return render(request, 'admins/admin_form.html', {'form': form, 'title': 'Crear Usuario'})

@admin_required
def admin_user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = AdminUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado con éxito.')
            return redirect('admins:admin_user_list')
    else:
        form = AdminUserUpdateForm(instance=user)
    return render(request, 'admins/admin_form.html', {'form': form, 'title': 'Editar Usuario'})

@admin_required
def admin_user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado con éxito.')
        return redirect('perfiles:admin_user_list')
    return render(request, 'perfiles/admin_confirm_delete.html', {'object': user, 'title': 'Eliminar Usuario'})

# CRUD para UserProfile
@admin_required
def admin_userprofile_list(request):
    userprofiles = UserProfile.objects.all()
    return render(request, 'admins/admin_userprofile_list.html', {'userprofiles': userprofiles})

@admin_required
def admin_userprofile_create(request):
    if request.method == 'POST':
        form = AdminUserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            userprofile = form.save()
            messages.success(request, 'Perfil de usuario creado con éxito.')
            return redirect('admins:admin_userprofile_list')
    else:
        form = AdminUserProfileForm()
    return render(request, 'admins/admin_form.html', {'form': form, 'title': 'Crear Perfil de Usuario'})

@admin_required
def admin_userprofile_edit(request, pk):
    userprofile = get_object_or_404(UserProfile, pk=pk)
    if request.method == 'POST':
        form = AdminUserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil de usuario actualizado con éxito.')
            return redirect('admins:admin_userprofile_list')
    else:
        form = AdminUserProfileForm(instance=userprofile)
    return render(request, 'admins/admin_form.html', {'form': form, 'title': 'Editar Perfil de Usuario'})

@admin_required
def admin_userprofile_delete(request, pk):
    userprofile = get_object_or_404(UserProfile, pk=pk)
    if request.method == 'POST':
        userprofile.delete()
        messages.success(request, 'Perfil de usuario eliminado con éxito.')
        return redirect('admins:admin_userprofile_list')
    return render(request, 'admins/admin_confirm_delete.html', {'object': userprofile, 'title': 'Eliminar Perfil de Usuario'})

# CRUD para Cliente
@admin_required
def admin_cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'admins/admin_cliente_list.html', {'clientes': clientes})

@admin_required
def admin_cliente_create(request):
    if request.method == 'POST':
        form = AdminClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, 'Cliente creado con éxito.')
            return redirect('admins:admin_cliente_list')
    else:
        form = AdminClienteForm()
    return render(request, 'admins/admin_form.html', {'form': form, 'title': 'Crear Cliente'})

@admin_required
def admin_cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = AdminClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado con éxito.')
            return redirect('admins:admin_cliente_list')
    else:
        form = AdminClienteForm(instance=cliente)
    return render(request, 'admins/admin_form.html', {'form': form, 'title': 'Editar Cliente'})

@admin_required
def admin_cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado con éxito.')
        return redirect('admins:admin_cliente_list')
    return render(request, 'admins/admin_confirm_delete.html', {'object': cliente, 'title': 'Eliminar Cliente'})

# CRUD para Vehiculo
@admin_required
def admin_vehiculo_list(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'admins/admin_vehiculo_list.html', {'vehiculos': vehiculos})

@admin_required
def admin_vehiculo_create(request):
    if request.method == 'POST':
        form = AdminVehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save()
            messages.success(request, 'Vehículo creado con éxito.')
            return redirect('admins:admin_vehiculo_list')
    else:
        form = AdminVehiculoForm()
    return render(request, 'admins/admin_form.html', {'form': form, 'title': 'Crear Vehículo'})

@admin_required
def admin_vehiculo_edit(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        form = AdminVehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo actualizado con éxito.')
            return redirect('admins:admin_vehiculo_list')
    else:
        form = AdminVehiculoForm(instance=vehiculo)
    return render(request, 'admins/admin_form.html', {'form': form, 'title': 'Editar Vehículo'})

@admin_required
def admin_vehiculo_delete(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        vehiculo.delete()
        messages.success(request, 'Vehículo eliminado con éxito.')
        return redirect('admins:admin_vehiculo_list')
    return render(request, 'admins/admin_confirm_delete.html', {'object': vehiculo, 'title': 'Eliminar Vehículo'})

# CRUD para Cita
@admin_required
def admin_cita_list(request):
    citas = Cita.objects.all()
    return render(request, 'perfiles/admin_cita_list.html', {'citas': citas})

@admin_required
def admin_cita_create(request):
    if request.method == 'POST':
        form = AdminCitaForm(request.POST)
        if form.is_valid():
            cita = form.save()
            messages.success(request, 'Cita creada con éxito.')
            return redirect('admins:admin_cita_list')
    else:
        form = AdminCitaForm()
    return render(request, 'admins/admin_form.html', {'form': form, 'title': 'Crear Cita'})

@admin_required
def admin_cita_edit(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        form = AdminCitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita actualizada con éxito.')
            return redirect('admins:admin_cita_list')
    else:
        form = AdminCitaForm(instance=cita)
    return render(request, 'admins/admin_form.html', {'form': form, 'title': 'Editar Cita'})

@admin_required
def admin_cita_delete(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        cita.delete()
        messages.success(request, 'Cita eliminada con éxito.')
        return redirect('admins:admin_cita_list')
    return render(request, 'admins/admin_confirm_delete.html', {'object': cita, 'title': 'Eliminar Cita'})

# CRUD para Servicio
@admin_required
def admin_servicio_list(request):
    servicios = Servicio.objects.all()
    return render(request, 'admins/admin_servicio_list.html', {'servicios': servicios})

@admin_required
def admin_servicio_create(request):
    if request.method == 'POST':
        form = AdminServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save()
            messages.success(request, 'Servicio creado con éxito.')
            return redirect('admins:admin_servicio_list')
    else:
        form = AdminServicioForm()
    return render(request, 'admins/admin_form.html', {'form': form, 'title': 'Crear Servicio'})

@admin_required
def admin_servicio_edit(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        form = AdminServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Servicio actualizado con éxito.')
            return redirect('admins:admin_servicio_list')
    else:
        form = AdminServicioForm(instance=servicio)
    return render(request, 'admins/admin_form.html', {'form': form, 'title': 'Editar Servicio'})

@admin_required
def admin_servicio_delete(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        servicio.delete()
        messages.success(request, 'Servicio eliminado con éxito.')
        return redirect('admins:admin_servicio_list')
    return render(request, 'perfiles/admin_confirm_delete.html', {'object': servicio, 'title': 'Eliminar Servicio'})

# CRUD para Empleado
@admin_required
def admin_empleado_list(request):
    empleados = Empleado.objects.all()
    return render(request, 'perfiles/admin_empleado_list.html', {'empleados': empleados})

@admin_required
def admin_empleado_create(request):
    if request.method == 'POST':
        form = AdminEmpleadoForm(request.POST)
        if form.is_valid():
            empleado = form.save()
            messages.success(request, 'Empleado creado con éxito.')
            return redirect('perfiles:admin_empleado_list')
    else:
        form = AdminEmpleadoForm()
    return render(request, 'perfiles/admin_form.html', {'form': form, 'title': 'Crear Empleado'})

@admin_required
def admin_empleado_edit(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        form = AdminEmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado actualizado con éxito.')
            return redirect('perfiles:admin_empleado_list')
    else:
        form = AdminEmpleadoForm(instance=empleado)
    return render(request, 'perfiles/admin_form.html', {'form': form, 'title': 'Editar Empleado'})

@admin_required
def admin_empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        messages.success(request, 'Empleado eliminado con éxito.')
        return redirect('perfiles:admin_empleado_list')
    return render(request, 'perfiles/admin_confirm_delete.html', {'object': empleado, 'title': 'Eliminar Empleado'})

# CRUD para EmployeeRequest
@admin_required
def admin_employee_request_list(request):
    employee_requests = EmployeeRequest.objects.all()
    return render(request, 'perfiles/admin_employee_request_list.html', {'employee_requests': employee_requests})

@admin_required
def admin_employee_request_create(request):
    if request.method == 'POST':
        form = AdminEmployeeRequestForm(request.POST)
        if form.is_valid():
            employee_request = form.save()
            messages.success(request, 'Solicitud de empleado creada con éxito.')
            return redirect('perfiles:admin_employee_request_list')
    else:
        form = AdminEmployeeRequestForm()
    return render(request, 'perfiles/admin_form.html', {'form': form, 'title': 'Crear Solicitud de Empleado'})

@admin_required
def admin_employee_request_edit(request, pk):
    employee_request = get_object_or_404(EmployeeRequest, pk=pk)
    if request.method == 'POST':
        form = AdminEmployeeRequestForm(request.POST, instance=employee_request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Solicitud de empleado actualizada con éxito.')
            return redirect('perfiles:admin_employee_request_list')
    else:
        form = AdminEmployeeRequestForm(instance=employee_request)
    return render(request, 'perfiles/admin_form.html', {'form': form, 'title': 'Editar Solicitud de Empleado'})

@admin_required
def admin_employee_request_delete(request, pk):
    employee_request = get_object_or_404(EmployeeRequest, pk=pk)
    if request.method == 'POST':
        employee_request.delete()
        messages.success(request, 'Solicitud de empleado eliminada con éxito.')
        return redirect('perfiles:admin_employee_request_list')
    return render(request, 'perfiles/admin_confirm_delete.html', {'object': employee_request, 'title': 'Eliminar Solicitud de Empleado'})

# Vista para Activity Logs
@admin_required
def admin_activity_log_list(request):
    activity_logs = ActivityLog.objects.all().order_by('-timestamp')
    return render(request, 'perfiles/admin_activity_log_list.html', {'activity_logs': activity_logs})