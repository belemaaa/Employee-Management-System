from django.db import models
from django.contrib.auth.models import AbstractUser


class Admin(AbstractUser):
    def __str__(self):
        return self.username
    
class Employee(models.Model):
    user = models.ForeignKey(Admin, on_delete=models.CASCADE, default=None)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(default='noemail@example.com')
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    sex = models.CharField(max_length=255)
    state_of_origin = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
