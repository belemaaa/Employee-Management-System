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
    employee_id = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'user',
            'employee_id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'address',
            'position',
            'sex',
            'state_of_origin',
            'date_of_birth',
            'created_at'
        ]
    
    def get_employee_id(self, obj):
        return {
            'id': obj.id
        }