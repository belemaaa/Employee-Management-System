from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.AdminSignup.as_view()),
    path('login/', views.AdminLogin.as_view()),
    path('employee/create/', views.CreateEmployee.as_view()),
    path('employee/view/', views.GetEmployees.as_view()),
    path('employee/detail/<int:employee_id>/', views.GetEmployeeDetails.as_view()),
    path('employee/update/<int:employee_id>/', views.UpdateEmployeeData.as_view()),
]