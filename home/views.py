from json import loads as json_loads

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.contrib.gis.geos import Point

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ProfileSerializer, PostSerializer
from .models import Profile, Posts

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {"msg": "Hello, you are in!"}
        return Response(content)


class ProfileView(APIView):
    permisson_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        data['location'] = Point(data['location'])
        serializer = ProfileSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)

    def get(self, request):
        profile = Profile.objects.get(user=request.user.id) 
        data = {
            'email': profile.user.email,
            'dob': profile.dob,
            'bio': profile.bio,
            'location': {
                'lat': profile.location.coords[0],
                'lon': profile.location.coords[1],
                },
            'tags': profile.tags,
        }
        
        # return JsonResponse(json_loads(response), safe=False)

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
