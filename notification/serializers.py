from rest_framework import serializers

from .models import UserNotifications

class ExpoTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

class UserNotificationsSerializer(serializers.ModelField):
    image = serializers.SerializerMethodField('get_image')

    def get_image(self, obj):
        if obj.event.image:
            return obj.event.image.url
        
        return None

    class Meta:
        model = UserNotifications
        fields = '__all__'