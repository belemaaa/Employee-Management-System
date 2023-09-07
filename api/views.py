from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from . import serializers
from . import models
from rest_framework import status


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
