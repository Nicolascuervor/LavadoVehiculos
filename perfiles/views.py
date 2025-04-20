# perfiles/views.py
from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import UserProfile, EmployeeRequest
from .serializers import UserProfileSerializer, EmployeeRequestSerializer, UserSerializer
from django.contrib.auth.decorators import login_required
from secciones.models import Cita, Servicio, Vehiculo, Cliente, Empleado
from secciones.forms import VehiculoForm

def custom_404(request, exception):
    return render(request, 'perfiles/404.html', status=404)

def custom_500(request):
    return render(request, 'perfiles/500.html', status=500)

# perfiles/views.py (fragmento relevante)
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear un cliente asociado con el usuario
            if Cliente.objects.filter(identificacion=form.cleaned_data['identification']).exists():
                messages.error(request, 'El identificador ya está en uso.')
                return render(request, 'perfiles/register.html', {'form': form})
            Cliente.objects.create(
                usuario=user,
                nombre=form.cleaned_data['first_name'] or 'Nombre',
                apellido=form.cleaned_data['last_name'] or 'Apellido',
                email=form.cleaned_data['email'],
                identificacion=form.cleaned_data['identification'],
                telefono=form.cleaned_data['telefono'],
            )
            login(request, user)
            messages.success(request, '¡Tu cuenta ha sido creada! Ahora puedes iniciar sesión.')
            return redirect('perfiles:dashboard')
        else:
            # Si el formulario no es válido, pasar los errores a la plantilla
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
        user_profile = UserProfile.objects.create(user=request.user, role='Cliente')

    vehiculos = Vehiculo.objects.filter(usuario=request.user, cliente=cliente, estado='A')
    vehiculo_form = VehiculoForm()
    MAX_VEHICULOS = 10
    puede_agregar = len(vehiculos) < MAX_VEHICULOS

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        photo_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)

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

        if user_form.is_valid() and photo_form.is_valid():
            user_form.save()
            photo_form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado con éxito!')
            return redirect('perfiles:profile')
        else:
            messages.error(request, 'Error al actualizar el perfil. Por favor, revisa los campos.')
    
    else:
        user_form = UserUpdateForm(instance=request.user)
        photo_form = ProfileUpdateForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'photo_form': photo_form,
        'vehiculos': vehiculos,
        'vehiculo_form': vehiculo_form,
        'puede_agregar': puede_agregar,
    }
    return render(request, 'perfiles/profile.html', context)

@login_required
def dashboard(request):
    user_profile = request.user.profile
    if user_profile.role == 'Cliente':
        citas_pendientes = Cita.objects.filter(cliente__user=request.user, estado='pendiente').count()
        servicios_completados = Servicio.objects.filter(cita__cliente__user=request.user, estado='completado').count()
        vehiculos_atendidos = Vehiculo.objects.filter(usuario=request.user, estado='A').count()
    else:
        citas_pendientes = Cita.objects.filter(estado='pendiente').count()
        servicios_completados = Servicio.objects.filter(estado='completado').count()
        vehiculos_atendidos = Vehiculo.objects.filter(estado='A').count()

    context = {
        'usuario': request.user,
        'citas_pendientes': citas_pendientes,
        'servicios_completados': servicios_completados,
        'vehiculos_atendidos': vehiculos_atendidos,
    }
    return render(request, 'perfiles/dashboard.html', context)

# Vistas de API
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)

class EmployeeRequestCreateView(generics.CreateAPIView):
    queryset = EmployeeRequest.objects.all()
    serializer_class = EmployeeRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if EmployeeRequest.objects.filter(user=self.request.user, status='pending').exists():
            raise serializers.ValidationError("Ya tienes una solicitud de empleado pendiente.")
        if Empleado.objects.filter(usuario=self.request.user).exists():
            raise serializers.ValidationError("Ya eres un empleado.")
        serializer.save(user=self.request.user)

class EmployeeRequestListView(generics.ListAPIView):
    serializer_class = EmployeeRequestSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return EmployeeRequest.objects.all()

class EmployeeRequestDetailView(generics.RetrieveUpdateAPIView):
    queryset = EmployeeRequest.objects.all()
    serializer_class = EmployeeRequestSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.status != 'pending':
            raise serializers.ValidationError("No puedes modificar una solicitud que ya ha sido procesada.")
        serializer.save()