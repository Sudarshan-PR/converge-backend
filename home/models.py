from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.gis.geos import Point

from django.contrib.auth import get_user_model
User = get_user_model()

from event.models import Events 


# Posts Model
class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField()
    title = models.CharField(max_length=30)
    desc = models.CharField(max_length=150)

# User Profile Model
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True)
    tags = ArrayField(models.CharField(max_length=15), blank=True, null=True)
    bio = models.TextField(max_length=100, blank=True)
    dob = models.DateField(blank=True, null=True, auto_now=False, auto_now_add=False)
    location = models.PointField(blank=True, null=True)
    invites = models.ManyToManyField(Events)

    def __str__(self):
        return self.user.email

