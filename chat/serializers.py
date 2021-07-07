from rest_framework import serializers

from django.contrib.auth import get_user_model
User = get_user_model()

from event.models import Events

class EventRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id', 'title', 'image', 'host', 'attendees']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']