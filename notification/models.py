from django.db import models
from django.contrib.auth import get_user_model
from event.models import Events

User = get_user_model()

class UserNotifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    token = models.CharField(null=True, blank=True)
    msg = models.CharField(null=True, blank=True)