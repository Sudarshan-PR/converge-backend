from django.db import models
from event.models import Events

from django.contrib.auth import get_user_model
User = get_user_model()

class Messages(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(null=False, blank=False, max_length=200)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True) # Created in server
    created_time_user = models.DateTimeField(blank=True, null=True) # Created time given by user

    def __str__(self):
        return f'{self.author}[{self.created_at}] : {self.body}'