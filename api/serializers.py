from rest_framework import serializers
from .models import Admin, Employee


class AdminSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['username', 'email', 'password']


class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'