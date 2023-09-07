from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.AdminSignup.as_view()),
    path('login/', views.AdminLogin.as_view()),
]