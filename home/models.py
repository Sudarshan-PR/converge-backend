from django.db import models

from django.contrib.postgres.fields import ArrayField

from django.contrib.auth import get_user_model
User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tags = ArrayField(models.CharField(max_length=15), blank=True)    
    bio = models.TextField(max_length=100, blank=True)
    dob = models.DateField(blank=True, null=True, auto_now=False, auto_now_add=False)
    location = models.CharField(blank=True, max_length=50)