# secciones/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Cliente, Vehiculo, Empleado, Jornada, TurnoEmpleado, TipoInsumo, Insumo,
    Inventario, TipoLavado, Servicio, ConsumoInsumo, Factura, Cita, Promocion,
    CargaTrabajoEmpleado
)

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'

class JornadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jornada
        fields = '__all__'

class TurnoEmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurnoEmpleado
        fields = '__all__'

class TipoInsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoInsumo
        fields = '__all__'

class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = '__all__'

class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = '__all__'

class TipoLavadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoLavado
        fields = '__all__'

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class ConsumoInsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumoInsumo
        fields = '__all__'

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'

class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = '__all__'

class PromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocion
        fields = '__all__'

class CargaTrabajoEmpleadoSerializer(serializers.ModelSerializer):
    trabajos_realizados = serializers.IntegerField()
    trabajos_no_terminados = serializers.IntegerField()

    class Meta:
        model = CargaTrabajoEmpleado
        fields = ['empleado', 'trabajos_realizados', 'trabajos_no_terminados']