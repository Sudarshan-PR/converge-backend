from rest_framework import serializers
from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model

from .models import Profile, Posts

User = get_user_model()

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

class PostSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_user_name')
    user_image = serializers.SerializerMethodField('get_user_image')

    def get_user_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    def get_user_image(self, obj):
        user_image = Profile.objects.get(user=obj.user.id).image
        if user_image:
            return user_image.url
        else:
            return None

    class Meta:
        model = Posts
        fields = '__all__'