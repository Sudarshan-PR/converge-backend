from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=100, blank=True)
    dob = models.DateField(blank=True, null=True, auto_now=False, auto_now_add=False)
    location = models.CharField(blank=True, max_length=50)