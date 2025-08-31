from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.conf import settings

class Roles(models.TextChoices):
    EMPLOYEE = "employee", "Employee"
    JOB_SEEKER = "job_seeker", "Job Seeker"


class User(AbstractUser):
    roles = models.CharField(max_length=255, choices=Roles.choices, default=Roles.JOB_SEEKER)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name}-{self.last_name}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to="profile/", blank=True, null=True)
    bio = models.TextField(max_length=100000, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name}-{self.user.last_name}"