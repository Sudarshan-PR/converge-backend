from rest_framework import serializers
from django.contrib.gis.geos import Point

from .models import Profile, Posts
from event.models import Events

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['dob', 'tags', 'image', 'bio', 'location']

    def save(self, userid):
        data = self.validated_data
        profile = Profile.objects.get(user=userid)

        for key, value in data.items():
            if key == 'location':
                value = Point(value)

            setattr(profile, key, value)

        profile.save()

        return profile

# Invites sent by user
class PendingRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'