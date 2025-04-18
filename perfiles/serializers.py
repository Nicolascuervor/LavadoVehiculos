# perfiles/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, EmployeeRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'photo', 'created_at', 'updated_at']

class EmployeeRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = EmployeeRequest
        fields = ['id', 'user', 'requested_rol', 'status', 'created_at', 'updated_at']