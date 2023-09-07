from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from . import serializers
from . import models
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class AdminSignup(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = serializers.AdminSignupSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('password')
            raw_password = serializer.validated_data.get('password')
            hashed_password = make_password(raw_password)

            user_exists = models.Admin.objects.filter(email=email)
            if user_exists:
                return Response({'error': 'email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(password=hashed_password)
            return Response({'message': 'admin created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AdminLogin(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = serializers.AdminLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            try:
                user = models.Admin.objects.get(username=username)
            except models.Admin.DoesNotExist:
                user = None
            if user is not None and check_password(password, user.password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({'message': 'login successful',
                                 'access_token': token.key}, status=status.HTTP_200_OK) 
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateEmployee(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = serializers.EmployeeSerializer(data=request.data)

        if serializer.is_valid():
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            email = serializer.validated_data.get('email')
            phone_number = serializer.validated_data.get('phone_number')
            employee_id = serializer.validated_data.get('employee_id')
            address = serializer.validated_data.get('address')
            position = serializer.validated_data.get('position')
            sex = serializer.validated_data.get('sex')
            state_of_origin = serializer.validated_data.get('state_of_origin')
            date_of_birth = serializer.validated_data.get('date_of_birth')

            serializer.save(user=self.request.user)
            return Response({'message': 'Employee creation was successful',
                             'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
