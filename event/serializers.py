from rest_framework import serializers
from django.contrib.gis.geos import Point

from .models import Events

class EventCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Events
        exclude = ['host','attendees','invites_sent']


class EventGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'

class EventPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        exclude = ['host','attendees','invites_sent']

    def save(self, eventid):
        data = self.validated_data
        event = Events.objects.get(id=eventid)

        for key, value in data.items():
            if key == 'location':
                value = Point(value)

            setattr(event, key, value)

            event.save()

        return data