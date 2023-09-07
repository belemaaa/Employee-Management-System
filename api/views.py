from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
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
