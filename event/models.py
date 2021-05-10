from itertools import chain

from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.gis.geos import Point

from django.contrib.auth import get_user_model
User = get_user_model()


class Events(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name='attending_users')
    title = models.CharField(blank=False, max_length=30)
    image = models.ImageField(blank=True)
    tags = ArrayField(models.CharField(max_length=15), blank=True, null=True)
    desc = models.TextField(max_length=100, blank=True)
    create_date = models.DateField(auto_now=True, auto_now_add=False)
    event_date = models.DateField(auto_now=False, auto_now_add=False)
    location = models.PointField(blank=True, null=True)
    addr = models.TextField(max_length=100)
    max_attendees = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.host} : {self.title}'

# class Attendance(models.Model):
#     event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='event')
#     attendee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
#     is_attending = models.BooleanField(default=False)

#     def __str__(self):
#         return f'{self.event} : {self.attendee} : {self.is_attending}'