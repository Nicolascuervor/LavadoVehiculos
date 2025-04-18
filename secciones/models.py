from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Models
class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    identificacion = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    ESTADOS = [('A', 'Activo'), ('I', 'Inactivo')]
    estado = models.CharField(max_length=1, choices=ESTADOS, default='A')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.identificacion})"
    
    
    def get_fields(self):
        return [
            self.id,
            self.nombre,
            self.apellido,
            self.email,
            self.telefono,
        ]
        
        
    def get_fields_detailed(self):
        return [
            ("ID", self.id),
            ("Nombre", self.nombre),
            ("Apellido", self.apellido),
            ("Correo Electrónico", self.email),
            ("Teléfono", self.telefono),
            ("Usuario", self.user.username),
        ]


class Vehiculo(models.Model):
    TIPO_CHOICES = [
        ('Carro', 'Carro'),
        ('Moto', 'Moto'),
        ('Camioneta', 'Camioneta'),
        ('Camion', 'Camión'),
        ('Bicicleta', 'Bicicleta'),
        ('Avioneta', 'Avioneta'),
        ('Barco', 'Barco'),
    ]
    TAMANIO_CHOICES = [
        ('Pequeño', 'Pequeño'),
        ('Mediano', 'Mediano'),
        ('Grande', 'Grande'),
        ('Extra Grande', 'Extra Grande'),
    ]
    ESTADO_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
    ]
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    tamanio = models.CharField(max_length=50, choices=TAMANIO_CHOICES)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    placa = models.CharField(max_length=20, unique=True)
    color = models.CharField(max_length=30, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tipo} {self.tamanio} {self.marca} {self.modelo} ({self.placa})"


class Empleado(models.Model):
    ROL_CHOICES = [
        ('Recepcionista', 'Recepcionista'),
        ('Lavador', 'Lavador'),
        ('Supervisor', 'Supervisor'),
    ]
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    identificacion = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    rol = models.CharField(max_length=50, choices=ROL_CHOICES, default='Lavador')
    ESTADOS = [('A', 'Activo'), ('I', 'Inactivo')]
    estado = models.CharField(max_length=1, choices=ESTADOS)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol}) - {self.estado}"


class Jornada(models.Model):
    ESTADO_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
    ]
    nombre = models.CharField(max_length=50, blank=True)
    hora_inicio = models.TimeField()
    hora_salida = models.TimeField()
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.hora_inicio} - {self.hora_salida})"


class TurnoEmpleado(models.Model):
    ESTADO_CHOICES = [
        ('A', 'Activo'),
        ('C', 'Cancelado'),
    ]
    dia = models.DateField()
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    jornada = models.ForeignKey(Jornada, on_delete=models.CASCADE)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='A')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.dia} - {self.empleado.nombre} ({self.jornada.hora_inicio} - {self.jornada.hora_salida})"


class TipoInsumo(models.Model):
    CATEGORIA_CHOICES = [
        ('Limpieza', 'Limpieza'),
        ('Cera', 'Cera'),
        ('Shampoo', 'Shampoo'),
        ('Otros', 'Otros'),
    ]
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, default='Otros')
    ESTADOS = [('A', 'Activo'), ('I', 'Inactivo')]
    estado = models.CharField(max_length=1, choices=ESTADOS)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.categoria}) - {self.estado}"


class Insumo(models.Model):
    UNIDAD_MEDIDA_CHOICES = [
        ('Litros', 'Litros'),
        ('Unidades', 'Unidades'),
        ('Gramos', 'Gramos'),
    ]
    tipo_insumo = models.ForeignKey(TipoInsumo, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=50, choices=UNIDAD_MEDIDA_CHOICES)
    ESTADOS = [('A', 'Activo'), ('I', 'Inactivo')]
    estado = models.CharField(max_length=1, choices=ESTADOS)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tipo_insumo.nombre} - {self.nombre} ({self.unidad_medida}) - {self.estado}"


class Inventario(models.Model):
    ESTADO_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
    ]
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    stock = models.IntegerField()
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    stock_minimo = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.insumo.nombre} - Stock: {self.stock} ({self.estado})"


class TipoLavado(models.Model):
    ESTADO_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
    ]
    nombre = models.CharField(max_length=50)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    insumos = models.ManyToManyField(Insumo)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} - {self.costo} ({self.estado})"


class Servicio(models.Model):
    ESTADO_CHOICES = [
        ('P', 'Pendiente'),
        ('E', 'En Proceso'),
        ('C', 'Completado'),
    ]
    fecha = models.DateField()
    emp_recibe = models.ForeignKey(
        Empleado, on_delete=models.CASCADE, related_name="recibe_servicios")
    emp_lava = models.ForeignKey(
        Empleado, on_delete=models.CASCADE, related_name="lava_servicios")
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    tipo_lavado = models.ForeignKey(TipoLavado, on_delete=models.CASCADE)
    hora_recibe = models.TimeField()
    hora_entrega = models.TimeField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='P')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.fecha} - {self.vehiculo.placa} ({self.tipo_lavado.nombre}) - {self.estado}"


class ConsumoInsumo(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.servicio.vehiculo.placa} - {self.insumo.nombre} ({self.cantidad})"


class Factura(models.Model):
    servicio = models.OneToOneField(Servicio, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    fecha_emision = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    ESTADOS = [('P', 'Pendiente'), ('C', 'Pagada')]
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Factura {self.id} - {self.cliente.nombre} ({self.total})"


class Cita(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    tipo_lavado = models.ForeignKey(TipoLavado, on_delete=models.CASCADE)
    ESTADOS = [('P', 'Pendiente'), ('C', 'Confirmada'), ('X', 'Cancelada')]
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cita {self.cliente.nombre} - {self.vehiculo.placa} ({self.fecha} {self.hora})"


class Promocion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    descuento = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo_lavado = models.ManyToManyField(TipoLavado)
    ESTADOS = [('A', 'Activo'), ('I', 'Inactivo')]
    estado = models.CharField(max_length=1, choices=ESTADOS, default='A')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.descuento}% off)"


class CargaTrabajoEmpleado(models.Model):
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE, related_name="carga_trabajo")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def trabajos_realizados(self):
        """
        Calcula el número de servicios completados por el empleado.
        """
        return Servicio.objects.filter(emp_lava=self.empleado, estado='C').count()

    @property
    def trabajos_no_terminados(self):
        """
        Calcula el número de servicios pendientes o en proceso del empleado.
        """
        return Servicio.objects.filter(emp_lava=self.empleado, estado__in=['P', 'E']).count()

    def __str__(self):
        return f"Carga de trabajo de {self.empleado.nombre} {self.empleado.apellido}"


# Señales para crear automáticamente registros de CargaTrabajoEmpleado
@receiver(post_save, sender=Empleado)
def crear_carga_trabajo_empleado(sender, instance, created, **kwargs):
    if created:
        CargaTrabajoEmpleado.objects.create(empleado=instance)