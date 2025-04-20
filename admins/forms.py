# perfiles/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from perfiles.models import UserProfile, EmployeeRequest, ActivityLog
from secciones.models import Cliente, Vehiculo, Cita, Servicio, Empleado

# Formularios existentes (mantenidos como están)
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'correo@ejemplo.com'}),
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ingrese su nombre'}),
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ingrese su apellido'}),
    )
    identification = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ingrese su número de identificación'}),
    )
    telefono = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ingrese su número de teléfono'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'identification', 'telefono', 'password1', 'password2']

    def clean_identification(self):
        identification = self.cleaned_data.get('identification')
        if Cliente.objects.filter(identificacion=identification).exists():
            raise forms.ValidationError("Este número de identificación ya está registrado.")
        return identification

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise forms.ValidationError("El número de teléfono debe contener solo dígitos.")
        if len(telefono) < 7:
            raise forms.ValidationError("El número de teléfono debe tener al menos 7 dígitos.")
        return telefono

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'correo@ejemplo.com'}),
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ingrese su nombre'}),
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ingrese su apellido'}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo']
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'class': 'input-field'}),
        }

class ClienteUpdateForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'email', 'identificacion', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ingrese su nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ingrese su apellido'}),
            'email': forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'correo@ejemplo.com'}),
            'identificacion': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ingrese su número de identificación'}),
            'telefono': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ingrese su número de teléfono'}),
        }

# Nuevos formularios para el Superpanel
class AdminUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-field'}),
            'email': forms.EmailInput(attrs={'class': 'input-field'}),
            'first_name': forms.TextInput(attrs={'class': 'input-field'}),
            'last_name': forms.TextInput(attrs={'class': 'input-field'}),
        }

class AdminUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-field'}),
            'email': forms.EmailInput(attrs={'class': 'input-field'}),
            'first_name': forms.TextInput(attrs={'class': 'input-field'}),
            'last_name': forms.TextInput(attrs={'class': 'input-field'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'input-field'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'input-field'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'input-field'}),
        }

class AdminUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'photo', 'role']
        widgets = {
            'user': forms.Select(attrs={'class': 'input-field'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'input-field'}),
            'role': forms.Select(attrs={'class': 'input-field'}),
        }

class AdminClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['usuario', 'nombre', 'apellido', 'email', 'identificacion', 'telefono', 'estado']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'input-field'}),
            'nombre': forms.TextInput(attrs={'class': 'input-field'}),
            'apellido': forms.TextInput(attrs={'class': 'input-field'}),
            'email': forms.EmailInput(attrs={'class': 'input-field'}),
            'identificacion': forms.TextInput(attrs={'class': 'input-field'}),
            'telefono': forms.TextInput(attrs={'class': 'input-field'}),
            'estado': forms.Select(attrs={'class': 'input-field'}),
        }

class AdminVehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['tipo', 'tamanio', 'marca', 'modelo', 'descripcion', 'placa', 'color', 'cliente', 'usuario', 'estado']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'input-field'}),
            'tamanio': forms.Select(attrs={'class': 'input-field'}),
            'marca': forms.TextInput(attrs={'class': 'input-field'}),
            'modelo': forms.TextInput(attrs={'class': 'input-field'}),
            'descripcion': forms.Textarea(attrs={'class': 'input-field'}),
            'placa': forms.TextInput(attrs={'class': 'input-field'}),
            'color': forms.TextInput(attrs={'class': 'input-field'}),
            'cliente': forms.Select(attrs={'class': 'input-field'}),
            'usuario': forms.Select(attrs={'class': 'input-field'}),
            'estado': forms.Select(attrs={'class': 'input-field'}),

        }

class AdminCitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['cliente', 'fecha', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'input-field'}),
            'fecha': forms.DateTimeInput(attrs={'class': 'input-field', 'type': 'datetime-local'}),
            'estado': forms.Select(attrs={'class': 'input-field'}),
        }

class AdminServicioForm(forms.ModelForm):
   pass

class AdminEmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['usuario', 'nombre', 'apellido', 'identificacion', 'fecha_nacimiento', 'email', 'rol', 'estado']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'input-field'}),
            'nombre': forms.TextInput(attrs={'class': 'input-field'}),
            'apellido': forms.TextInput(attrs={'class': 'input-field'}),
            'identificacion': forms.TextInput(attrs={'class': 'input-field'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'input-field', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'input-field'}),
            'rol': forms.Select(attrs={'class': 'input-field'}),
            'estado': forms.Select(attrs={'class': 'input-field'}),
        }

class AdminEmployeeRequestForm(forms.ModelForm):
    class Meta:
        model = EmployeeRequest
        fields = ['user', 'requested_rol', 'status', 'reason']
        widgets = {
            'user': forms.Select(attrs={'class': 'input-field'}),
            'requested_rol': forms.Select(attrs={'class': 'input-field'}),
            'status': forms.Select(attrs={'class': 'input-field'}),
            'reason': forms.Textarea(attrs={'class': 'input-field'}),
        }