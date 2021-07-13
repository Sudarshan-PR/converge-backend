from rest_framework import serializers

from .models import UserNotifications

class ExpoTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

class UserNotificationsSerializer(serializers.ModelField):
    event_image = serializers.SerializerMethodField('get_event_image')

    def get_event_image(self, obj):
        if obj.event.image:
            return obj.event.image.url
        
        return None

    class Meta:
        model = UserNotifications
        fields = '__all__'