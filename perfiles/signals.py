# perfiles/signals.py
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out

# Función auxiliar para registrar actividades
def log_activity(user, action, model_name, object_id=None, description=None):
    # Importar ActivityLog dentro de la función para evitar importación circular
    from .models import ActivityLog
    ActivityLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=str(object_id) if object_id else None,
        description=description or f"{action} en {model_name} (ID: {object_id})",
    )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print("Señal create_user_profile activada para:", instance.username)
        try:
            # Importar UserProfile dentro de la función
            from .models import UserProfile
            user_profile = UserProfile.objects.create(user=instance, role='cliente')
            print("UserProfile creado para:", instance.username)
            log_activity(
                user=instance,
                action='CREATE',
                model_name='UserProfile',
                object_id=user_profile.id,
                description=f"Se creó el perfil de usuario para {instance.username}"
            )
        except Exception as e:
            print("Error al crear UserProfile:", str(e))

@receiver(post_save, sender=None, dispatch_uid="create_cliente_for_user_profile")
def create_cliente_for_user_profile(sender, instance, created, **kwargs):
    # Importar UserProfile dinámicamente
    from .models import UserProfile
    if sender != UserProfile:
        return
    if created and instance.role == 'cliente':
        print("Señal create_cliente_for_user_profile activada para:", instance.user.username)
        try:
            from secciones.models import Cliente
            if not Cliente.objects.filter(usuario=instance.user).exists():
                cliente = Cliente.objects.create(
                    usuario=instance.user,
                    nombre=instance.user.first_name or 'Nombre',
                    apellido=instance.user.last_name or 'Apellido',
                    email=instance.user.email,
                    identificacion=instance.user.identification,
                    telefono=instance.user.telefono,
                )
                print("Cliente creado para:", instance.user.username)
                log_activity(
                    user=instance.user,
                    action='CREATE',
                    model_name='Cliente',
                    object_id=cliente.id,
                    description=f"Se creó el cliente para {instance.user.username}"
                )
        except Exception as e:
            print("Error al crear Cliente:", str(e))

@receiver(post_save, sender=None, dispatch_uid="create_empleado_on_approval")
def create_empleado_on_approval(sender, instance, **kwargs):
    # Importar EmployeeRequest dinámicamente
    from .models import EmployeeRequest
    if sender != EmployeeRequest:
        return
    if instance.status == 'approved':
        print("Señal create_empleado_on_approval activada para:", instance.user.username)
        try:
            from secciones.models import Empleado
            if not Empleado.objects.filter(usuario=instance.user).exists():
                empleado = Empleado.objects.create(
                    usuario=instance.user,
                    nombre=instance.user.first_name or 'Nombre',
                    apellido=instance.user.last_name or 'Apellido',
                    identificacion=f"EMP-{instance.user.id}-{instance.requested_rol}",
                    fecha_nacimiento=None,
                    email=instance.user.email,
                    rol=instance.requested_rol.lower(),
                    estado='A'
                )
                print("Empleado creado para:", instance.user.username)
                log_activity(
                    user=instance.user,
                    action='CREATE',
                    model_name='Empleado',
                    object_id=empleado.id,
                    description=f"Se creó el empleado para {instance.user.username} con rol {instance.requested_rol}"
                )
        except Exception as e:
            print("Error al crear Empleado:", str(e))

# Registrar acciones CRUD para los modelos principales
@receiver(post_save, sender=User)
def log_user_save(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    log_activity(
        user=instance,
        action=action,
        model_name='User',
        object_id=instance.id,
        description=f"Usuario {instance.username} {'creado' if created else 'actualizado'}"
    )

@receiver(post_save, sender=None, dispatch_uid="log_userprofile_save")
def log_userprofile_save(sender, instance, created, **kwargs):
    from .models import UserProfile
    if sender != UserProfile:
        return
    if not created:  # Ya se maneja en create_user_profile
        log_activity(
            user=instance.user,
            action='UPDATE',
            model_name='UserProfile',
            object_id=instance.id,
            description=f"Perfil de usuario actualizado para {instance.user.username}"
        )

@receiver(post_save, sender=None, dispatch_uid="log_cliente_save")
def log_cliente_save(sender, instance, created, **kwargs):
    from secciones.models import Cliente
    if sender != Cliente:
        return
    if not created:  # Ya se maneja en create_cliente_for_user_profile
        log_activity(
            user=instance.usuario,
            action='UPDATE',
            model_name='Cliente',
            object_id=instance.id,
            description=f"Cliente actualizado para {instance.nombre} {instance.apellido}"
        )

@receiver(post_save, sender=None, dispatch_uid="log_vehiculo_save")
def log_vehiculo_save(sender, instance, created, **kwargs):
    from secciones.models import Vehiculo
    if sender != Vehiculo:
        return
    action = 'CREATE' if created else 'UPDATE'
    log_activity(
        user=instance.usuario,
        action=action,
        model_name='Vehiculo',
        object_id=instance.id,
        description=f"Vehículo {instance.placa} {'creado' if created else 'actualizado'} por {instance.usuario.username}"
    )

@receiver(post_save, sender=None, dispatch_uid="log_cita_save")
def log_cita_save(sender, instance, created, **kwargs):
    from secciones.models import Cita
    if sender != Cita:
        return
    action = 'CREATE' if created else 'UPDATE'
    log_activity(
        user=instance.cliente.usuario if instance.cliente else None,
        action=action,
        model_name='Cita',
        object_id=instance.id,
        description=f"Cita {instance.id} {'creada' if created else 'actualizada'} para cliente {instance.cliente}"
    )

@receiver(post_save, sender=None, dispatch_uid="log_servicio_save")
def log_servicio_save(sender, instance, created, **kwargs):
    from secciones.models import Servicio
    if sender != Servicio:
        return
    action = 'CREATE' if created else 'UPDATE'
    log_activity(
        user=None,  # Puede asignarse al empleado que realiza el servicio
        action=action,
        model_name='Servicio',
        object_id=instance.id,
        description=f"Servicio {instance.id} {'creado' if created else 'actualizado'} para cita {instance.cita}"
    )

@receiver(post_save, sender=None, dispatch_uid="log_empleado_save")
def log_empleado_save(sender, instance, created, **kwargs):
    from secciones.models import Empleado
    if sender != Empleado:
        return
    if not created:  # Ya se maneja en create_empleado_on_approval
        log_activity(
            user=instance.usuario,
            action='UPDATE',
            model_name='Empleado',
            object_id=instance.id,
            description=f"Empleado actualizado para {instance.nombre} {instance.apellido}"
        )

@receiver(post_save, sender=None, dispatch_uid="log_employee_request_save")
def log_employee_request_save(sender, instance, created, **kwargs):
    from .models import EmployeeRequest
    if sender != EmployeeRequest:
        return
    action = 'CREATE' if created else 'UPDATE'
    if not (created and instance.status == 'approved'):  # Ya se maneja en create_empleado_on_approval
        log_activity(
            user=instance.user,
            action=action,
            model_name='EmployeeRequest',
            object_id=instance.id,
            description=f"Solicitud de empleado {instance.requested_rol} {'creada' if created else 'actualizada'} por {instance.user.username}"
        )

# Registrar eliminaciones
@receiver(pre_delete, sender=User)
def log_user_delete(sender, instance, **kwargs):
    log_activity(
        user=instance,
        action='DELETE',
        model_name='User',
        object_id=instance.id,
        description=f"Usuario {instance.username} eliminado"
    )

@receiver(pre_delete, sender=None, dispatch_uid="log_userprofile_delete")
def log_userprofile_delete(sender, instance, **kwargs):
    from .models import UserProfile
    if sender != UserProfile:
        return
    log_activity(
        user=instance.user,
        action='DELETE',
        model_name='UserProfile',
        object_id=instance.id,
        description=f"Perfil de usuario eliminado para {instance.user.username}"
    )

@receiver(pre_delete, sender=None, dispatch_uid="log_cliente_delete")
def log_cliente_delete(sender, instance, **kwargs):
    from secciones.models import Cliente
    if sender != Cliente:
        return
    log_activity(
        user=instance.usuario,
        action='DELETE',
        model_name='Cliente',
        object_id=instance.id,
        description=f"Cliente eliminado: {instance.nombre} {instance.apellido}"
    )

@receiver(pre_delete, sender=None, dispatch_uid="log_vehiculo_delete")
def log_vehiculo_delete(sender, instance, **kwargs):
    from secciones.models import Vehiculo
    if sender != Vehiculo:
        return
    log_activity(
        user=instance.usuario,
        action='DELETE',
        model_name='Vehiculo',
        object_id=instance.id,
        description=f"Vehículo {instance.placa} eliminado por {instance.usuario.username}"
    )

@receiver(pre_delete, sender=None, dispatch_uid="log_cita_delete")
def log_cita_delete(sender, instance, **kwargs):
    from secciones.models import Cita
    if sender != Cita:
        return
    log_activity(
        user=instance.cliente.usuario if instance.cliente else None,
        action='DELETE',
        model_name='Cita',
        object_id=instance.id,
        description=f"Cita {instance.id} eliminada para cliente {instance.cliente}"
    )

@receiver(pre_delete, sender=None, dispatch_uid="log_servicio_delete")
def log_servicio_delete(sender, instance, **kwargs):
    from secciones.models import Servicio
    if sender != Servicio:
        return
    log_activity(
        user=None,
        action='DELETE',
        model_name='Servicio',
        object_id=instance.id,
        description=f"Servicio {instance.id} eliminado para cita {instance.cita}"
    )

@receiver(pre_delete, sender=None, dispatch_uid="log_empleado_delete")
def log_empleado_delete(sender, instance, **kwargs):
    from secciones.models import Empleado
    if sender != Empleado:
        return
    log_activity(
        user=instance.usuario,
        action='DELETE',
        model_name='Empleado',
        object_id=instance.id,
        description=f"Empleado eliminado: {instance.nombre} {instance.apellido}"
    )

@receiver(pre_delete, sender=None, dispatch_uid="log_employee_request_delete")
def log_employee_request_delete(sender, instance, **kwargs):
    from .models import EmployeeRequest
    if sender != EmployeeRequest:
        return
    log_activity(
        user=instance.user,
        action='DELETE',
        model_name='EmployeeRequest',
        object_id=instance.id,
        description=f"Solicitud de empleado {instance.requested_rol} eliminada por {instance.user.username}"
    )

# Registrar inicios y cierres de sesión
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    log_activity(
        user=user,
        action='LOGIN',
        model_name='User',
        object_id=user.id,
        description=f"Usuario {user.username} inició sesión"
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    log_activity(
        user=user,
        action='LOGOUT',
        model_name='User',
        object_id=user.id,
        description=f"Usuario {user.username} cerró sesión"
    )