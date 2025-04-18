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


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada con éxito! Bienvenido, {username}.')
            return redirect('login')  # Redirigir al login después del registro
    else:
        form = UserRegisterForm()
    return render(request, 'perfiles/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        photo_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and photo_form.is_valid():
            user_form.save()
            photo_form.save()
            messages.success(request, f'¡Tu perfil ha sido actualizado con éxito!')
            return redirect('perfiles:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        photo_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'perfiles/profile.html', {'user_form': user_form, 'photo_form': photo_form})


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