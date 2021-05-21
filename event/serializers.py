from rest_framework import serializers
from django.contrib.gis.geos import Point

from .models import Events

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        exclude = ['host','attendees']


class EventGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'