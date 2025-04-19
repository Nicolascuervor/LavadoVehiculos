# perfiles/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile




class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']  # Quitamos 'password'

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # Crear o actualizar el perfil con el rol por defecto 'cliente'
            profile, created = UserProfile.objects.get_or_create(user=user)
            if created:  # Solo asignar el rol si el perfil es nuevo
                profile.role = 'cliente'  # Rol por defecto
                profile.save()
        return user
    
    

