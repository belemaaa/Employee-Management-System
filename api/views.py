from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from rest_framework import status
from .authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from cloudinary.uploader import upload
from django.db.models import Q
from functools import reduce
from operator import or_
from . import serializers
from . import models

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
                                 'user_id': user.id,
                                 'access_token': token.key}, status=status.HTTP_200_OK) 
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateEmployee(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = serializers.EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            email = serializer.validated_data.get('email')
            phone_number = serializer.validated_data.get('phone_number')
            address = serializer.validated_data.get('address')
            position = serializer.validated_data.get('position')
            sex = serializer.validated_data.get('sex')
            state_of_origin = serializer.validated_data.get('state_of_origin')
            date_of_birth = serializer.validated_data.get('date_of_birth')
            image = request.data.get('image')
            if image:
                # upload the image to Cloudinary
                uploaded_image = upload(image)
                serializer.validated_data['image'] = uploaded_image['secure_url']
            else:
                serializer.validated_data.pop('image', None)

            serializer.save(user=self.request.user)
            return Response({'message': 'Employee creation was successful',
                             'employee_data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)

class GetEmployees(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        queryset = models.Employee.objects.filter(user=user)
        serializer = serializers.EmployeeSerializer(queryset, many=True)
        
        return Response({'employee_data': serializer.data}, status=status.HTTP_200_OK)

class GetEmployeeDetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, employee_id):
        try:
            user = request.user
            queryset = models.Employee.objects.get(id=employee_id, user=user)
            serializer = serializers.EmployeeSerializer(queryset, many=False)
            return Response({'Employee_data': serializer.data}, status=status.HTTP_200_OK)
        
        except models.Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

class UpdateEmployeeData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, employee_id):
        try:
            user = request.user
            employee = models.Employee.objects.get(id=employee_id, user=user)
            serializer = serializers.EmployeeSerializer(employee, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Employee data updated.',
                                 'Employee_data': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.Employee.DoesNotExist:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class SearchEmployee(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        search_query = self.request.query_params.get('q', None)
        queryset = models.Employee.objects.filter(user=user)
        if search_query:
            search_parts = search_query.split()

            if len(search_parts) == 2:
                first_name, last_name = search_parts
                queryset = queryset.filter(Q(first_name__icontains=first_name) & Q(last_name__icontains=last_name))
            else:
                query_parts = [Q(first_name__icontains=part) | Q(last_name__icontains=part) for part in search_parts]
                combined_query = reduce(or_, query_parts)
                queryset = queryset.filter(combined_query)
        serializer = serializers.EmployeeSerializer(queryset, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
class DeleteEmployee(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, employee_id):
        try:
            user = request.user
            employee = models.Employee.objects.get(id=employee_id, user=user)
            employee.delete()
            return Response({'message': 'Employee deleted successfully.'}, status=status.HTTP_200_OK)
        except models.Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)