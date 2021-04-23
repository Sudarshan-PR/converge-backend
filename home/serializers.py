from rest_framework import serializers
from django.contrib.gis.geos import Point

from .models import Profile, Posts

class ProfileUpdateSerializer(serializers.Serializer):
    dob = serializers.DateField()
    image = serializers.ImageField()
    bio = serializers.CharField(max_length=100, allow_blank=True)
    tags = serializers.StringRelatedField(many=True)

    def update(self, request, validated_data):
        validated_data['user'] = request.user.id
        profile = Profile(validated_data)
        profile.save()

    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['dob', 'tags', 'image', 'bio', 'location']

    def save(self, userid):
        data = self.validated_data
        profile = Profile.objects.get(user=userid)

        for key, value in data.items():
            if key is 'location':
                value = Point(value)
                
            setattr(profile, key, value)

        profile.save()

        return profile

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'