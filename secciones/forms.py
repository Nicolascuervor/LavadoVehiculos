# secciones/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from perfiles.models import UserProfile
from .models import Vehiculo


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UserProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo']
        
        
        
class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['tipo', 'tamanio', 'marca', 'modelo', 'descripcion', 'placa', 'color']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-input w-full p-2 border rounded'}),
            'tamanio': forms.Select(attrs={'class': 'form-input w-full p-2 border rounded'}),
            'marca': forms.TextInput(attrs={'class': 'form-input w-full p-2 border rounded'}),
            'modelo': forms.TextInput(attrs={'class': 'form-input w-full p-2 border rounded'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-input w-full p-2 border rounded'}),
            'placa': forms.TextInput(attrs={'class': 'form-input w-full p-2 border rounded'}),
            'color': forms.TextInput(attrs={'class': 'form-input w-full p-2 border rounded'}),
        }