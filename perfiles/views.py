from django.shortcuts import render

# Create your views here.
# perfiles/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import UserProfile, EmployeeRequest
from .serializers import UserProfileSerializer, EmployeeRequestSerializer, UserSerializer, serializers
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from secciones.models import Cita, Servicio, Vehiculo


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from secciones.models import Vehiculo, Cliente
from secciones.forms import VehiculoForm



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear un cliente asociado con el usuario
            Cliente.objects.create(
                user=user,
                nombre=user.first_name,
                apellido=user.last_name,
                email=user.email,
                identificacion=user.username,
                telefono='',
                
            )
            login(request, user)
            messages.success(request, f'¡Tu cuenta ha sido creada! Ahora puedes iniciar sesión.')
            return redirect('perfiles:dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'perfiles/register.html', {'form': form})

@login_required
def profile(request):
  
  # Obtener el cliente asociado con el usuario
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        # Si no existe un cliente asociado, podrías crearlo aquí o manejar el error
        messages.error(request, 'No tienes un cliente asociado. Contacta al administrador.')
        return redirect('perfiles:dashboard')

    # Obtener los vehículos del usuario (filtrados por usuario y cliente)
    vehiculos = Vehiculo.objects.filter(usuario=request.user, cliente=cliente, estado='A')
    vehiculo_form = VehiculoForm()
    # Límite de 10 vehículos
    MAX_VEHICULOS = 10
    puede_agregar = len(vehiculos) < MAX_VEHICULOS

    # Manejo de operaciones CRUD para vehículos
    if request.method == 'POST':
        # Actualización del perfil (como antes)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        photo_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if 'action' in request.POST:
            action = request.POST.get('action')
            vehiculo_id = request.POST.get('vehiculo_id')

            if action == 'create' and puede_agregar:
                vehiculo_form = VehiculoForm(request.POST)
                if vehiculo_form.is_valid():
                    vehiculo = vehiculo_form.save(commit=False)
                    vehiculo.usuario = request.user
                    vehiculo.cliente = cliente
                    vehiculo.estado = 'A'  # Activo por defecto
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
                vehiculo.estado = 'I'  # Cambiar estado a Inactivo en lugar de eliminar
                vehiculo.save()
                messages.success(request, 'Vehículo marcado como inactivo.')
                return redirect('perfiles:profile')

        # Actualización del perfil (como antes)
        if user_form.is_valid() and photo_form.is_valid():
            user_form.save()
            photo_form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado con éxito!')
            return redirect('perfiles:profile')
        else:
            messages.error(request, 'Error al actualizar el perfil. Por favor, revisa los campos.')
    
    else:
        user_form = UserUpdateForm(instance=request.user)
        photo_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'photo_form': photo_form,
        'vehiculos': vehiculos,
        'vehiculo_form': vehiculo_form,
        'puede_agregar': puede_agregar,
    }
    return render(request, 'perfiles/profile.html', context)

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
        from secciones.models import Empleado
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
        
     
@login_required
def dashboard(request):
    # Calcular métricas dinámicas
    citas_pendientes = Cita.objects.filter(estado='pendiente').count()
    servicios_completados = Servicio.objects.filter(estado='completado').count()
    vehiculos_atendidos = Vehiculo.objects.count()  # Simplificado, puedes ajustarlo según tu lógica

    context = {
        'user': request.user,
        'citas_pendientes': citas_pendientes,
        'servicios_completados': servicios_completados,
        'vehiculos_atendidos': vehiculos_atendidos,
    }
    return render(request, 'perfiles/dashboard.html', context)