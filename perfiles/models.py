# perfiles/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ActivityLog(models.Model):
    ACTION_CHOICES = (
        ('CREATE', 'Creación'),
        ('UPDATE', 'Actualización'),
        ('DELETE', 'Eliminación'),
        ('LOGIN', 'Inicio de Sesión'),
        ('LOGOUT', 'Cierre de Sesión'),
        ('OTHER', 'Otro'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_logs')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=50)  # Nombre del modelo afectado (User, Cliente, etc.)
    object_id = models.CharField(max_length=50, blank=True, null=True)  # ID del objeto afectado
    description = models.TextField()  # Descripción detallada del movimiento
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username if self.user else 'Sistema'} - {self.action} - {self.model_name} - {self.timestamp}"


from . import signals  # Importar las señales aquí para evitar problemas de importación circular


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('lavador', 'Lavador'),
        ('recepcionista', 'Recepcionista'),
        ('supervisor', 'Supervisor'),
        ('cliente', 'Cliente'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile/', blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cliente')

    def __str__(self):
        return f'Perfil de {self.user.username}'

class EmployeeRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
    )
    ROL_CHOICES = [
        ('recepcionista', 'Recepcionista'),
        ('lavador', 'Lavador'),
        ('supervisor', 'Supervisor'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_requests')
    requested_rol = models.CharField(max_length=50, choices=ROL_CHOICES, default='lavador')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True, null=True)  # Campo para el motivo de la solicitud
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Solicitud de {self.user.username} para {self.requested_rol} - {self.status}"

# Señal para crear un UserProfile cuando se crea un User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role='cliente')
        
        

# Señal para crear un Cliente cuando se crea un UserProfile con rol 'cliente'
@receiver(post_save, sender=UserProfile)
def create_cliente_for_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'cliente':
        print("Señal create_cliente_for_user_profile activada para:", instance.user.username)  # Depuración
        try:
            from secciones.models import Cliente
            if not Cliente.objects.filter(usuario=instance.user).exists():
                Cliente.objects.create(
                    usuario=instance.user,
                    nombre=instance.user.first_name or 'Nombre',
                    apellido=instance.user.last_name or 'Apellido',
                    email=instance.user.email,
                    identificacion=instance.user.identification if hasattr(instance.user, 'identification') else 'Sin identificación',
                    telefono=instance.user.profile.telefono if hasattr(instance.user, 'profile') else 'Sin teléfono',
                )
                print("Cliente creado para:", instance.user.username)
        except Exception as e:
            print("Error al crear Cliente:", str(e))

# Señal para crear un Empleado automáticamente cuando se aprueba una solicitud
@receiver(post_save, sender=EmployeeRequest)
def create_empleado_on_approval(sender, instance, **kwargs):
    if instance.status == 'approved':
        from secciones.models import Empleado
        if not Empleado.objects.filter(usuario=instance.user).exists():
            Empleado.objects.create(
                usuario=instance.user,
                nombre=instance.user.first_name or 'Nombre',
                apellido=instance.user.last_name or 'Apellido',
                identificacion=f"EMP-{instance.user.id}-{instance.requested_rol}",  # Identificador más claro
                fecha_nacimiento=None,
                email=instance.user.email,
                rol=instance.requested_rol.lower(),
                estado='A'
            )