# perfiles/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

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
        from secciones.models import Cliente
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
        fields = ['username','first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo']
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'class': 'input-field'}),
        }