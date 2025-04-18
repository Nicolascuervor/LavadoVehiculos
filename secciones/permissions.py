# secciones/permissions.py
from rest_framework import permissions
from .models import Empleado, Cliente, Vehiculo, Servicio

class IsSuperUserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)

class IsLavador(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            empleado = Empleado.objects.get(usuario=request.user)
            return empleado.rol == 'Lavador' and empleado.estado == 'A'
        except Empleado.DoesNotExist:
            return False

class IsRecepcionista(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            empleado = Empleado.objects.get(usuario=request.user)
            return empleado.rol == 'Recepcionista' and empleado.estado == 'A'
        except Empleado.DoesNotExist:
            return False

class IsSupervisor(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            empleado = Empleado.objects.get(usuario=request.user)
            return empleado.rol == 'Supervisor' and empleado.estado == 'A'
        except Empleado.DoesNotExist:
            return False

class IsCliente(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        empleado_exists = Empleado.objects.filter(usuario=request.user).exists()
        if empleado_exists:
            return False
        try:
            cliente = Cliente.objects.get(usuario=request.user)
            return cliente.estado == 'A'
        except Cliente.DoesNotExist:
            return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.usuario == request.user

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.usuario == request.user

class IsRelatedToServicio(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        try:
            empleado = Empleado.objects.get(usuario=request.user)
            if isinstance(obj, Vehiculo):
                return Servicio.objects.filter(emp_lava=empleado, vehiculo=obj, estado__in=['P', 'E']).exists()
            elif isinstance(obj, Cliente):
                return Servicio.objects.filter(emp_lava=empleado, vehiculo__cliente=obj, estado__in=['P', 'E']).exists()
            return False
        except Empleado.DoesNotExist:
            return False