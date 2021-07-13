from django.db import models
from django.contrib.auth import get_user_model
from event.models import Events

User = get_user_model()

class UserNotifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    msg = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f'[{self.created_at}] {self.user}: {self.event.title}'
    

class ExpoToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user} : {self.token} : {self.active}'