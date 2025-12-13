from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    year_of_admission = models.PositiveIntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to="profiles/", blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"
