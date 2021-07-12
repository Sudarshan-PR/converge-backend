from rest_framework import serializers

class ExpoTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    