from rest_framework import serializers

from .models import UserNotifications

class ExpoTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

class UserNotificationsSerializer(serializers.ModelField):
    class Meta:
        model = UserNotifications
        fields = '__all__'