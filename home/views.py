from json import loads as json_loads

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.contrib.gis.geos import Point

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ProfileSerializer, PostSerializer, ProfileUpdateSerializer
from .models import Profile, Posts

class HelloView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {"msg": "Hello, you are in!"}
        return Response(content)


class ProfileView(APIView):
    permisson_classes = (IsAuthenticated,)

    def put(self, request):
        data = request.data

        serializer = ProfileSerializer(data=data)
       
        if serializer.is_valid():
            profile = serializer.save(request.user.id)            
            return Response({'msg': 'Profile has been updated!','user': request.user.id})

        return Response(serializer.errors)

    def get(self, request):
        profile = Profile.objects.get(user=request.user.id) 
        
        # Test if profile image exists
        try:
            image = profile.image.url
        except:
            image = None

        data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'profile_picture': image,
            'email': profile.user.email,
            'dob': profile.dob,
            'bio': profile.bio,
            'tags': profile.tags,
            'location': [profile.location.x, profile.location.y]
        }
        
        return Response(data)

class PostsView(APIView):
    def get(self, request):
        posts = Posts.objects.get(title="test 4")
        return HttpResponse(f'<img src={posts.image.url} alt="Image not shown" ></img>')

    def post(self, request):
        data = request.data
        data['user'] = request.user.id 
        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            currPost = Posts.objects.get(title=data['title'])
            return Response({'title':currPost.title, 'image':str(currPost.image)})

        return Response(serializer.errors)
