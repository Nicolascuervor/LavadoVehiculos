# perfiles/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('lavador', 'Lavador'),
        ('recepcionista', 'Recepcionista'),
        ('supervisor', 'Supervisor'),
        ('cliente', 'Cliente'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
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
        ('recepcionista', 'Recepcionista'),  # Usar minúsculas para consistencia
        ('lavador', 'Lavador'),
        ('supervisor', 'Supervisor'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_requests')
    requested_rol = models.CharField(max_length=50, choices=ROL_CHOICES, default='lavador')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Solicitud de {self.user.username} para {self.requested_rol} - {self.status}"

# Señal para crear o asegurar un UserProfile cuando se crea un User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # Asegurarse de que el perfil exista incluso si el usuario ya existía
        UserProfile.objects.get_or_create(user=instance)

# Señal para crear un Empleado automáticamente cuando se aprueba una solicitud
@receiver(post_save, sender=EmployeeRequest)
def create_empleado_on_approval(sender, instance, **kwargs):
    if instance.status == 'approved':
        # Importar aquí para evitar posibles dependencias circulares
        from secciones.models import Empleado
        if not Empleado.objects.filter(usuario=instance.user).exists():
            Empleado.objects.create(
                usuario=instance.user,
                nombre=instance.user.first_name or 'Nombre',
                apellido=instance.user.last_name or 'Apellido',
                identificacion=f"{instance.user.id}-{instance.requested_rol}",
                fecha_nacimiento=None,  # Hacer este campo nullable en el modelo Empleado
                email=instance.user.email,
                rol=instance.requested_rol.lower(),  # Asegurar consistencia en minúsculas
                estado='A'
            )