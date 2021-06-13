from django.http import HttpResponse
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import ProfileSerializer, PostSerializer
from .models import Profile, Posts
from register.models import User
from register.serializer import UserRegisterSerializer
from event.models import Events

import logging

logger = logging.getLogger('debug_logger')

class HelloView(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {"msg": "Hello, you are in!"}
        logger.debug("asdfasdfasfasdfasdf adfdafasdf hello")
        return Response(content)


class ProfileView(APIView):
    permisson_classes = [IsAuthenticated,]

    def put(self, request):
        data = request.data

        serializer = ProfileSerializer(data=data)
       
        if serializer.is_valid():
            profile = serializer.save(request.user.id)
            
            profile = ProfileSerializer(profile)

            msg = {'msg': 'Profile has been updated!','user': request.user.id}
            resp = dict(profile.data, **msg)
            
            return Response(resp)

        return Response(serializer.errors)

    def get(self, request):
        profile = Profile.objects.get(user=request.user.id)        
        # Test is coordinates are present
        try:
            loc = {'lon': profile.location.x, 'lat': profile.location.y}
        except Exception as e:
            loc = None

        profile = ProfileSerializer(profile)
        user = UserRegisterSerializer(request.user)

        # Note: As the 2 dicts are being merged, profile_ID is over-written by user_ID here
        profile = dict(profile.data, **user.data)

        profile['location'] = loc 
        
        invites = Events.objects.filter(invites_sent__invited_users=1)
        if invites:
            profile['invites'] = str(invites)
        except ObjectDoesNotExist:
            profile['invites'] = []
        
        return Response(profile)

@api_view()
def get_user_profile(request, userid):
    user, profile = None, None
    try:
        user = User.objects.get(id=userid)
        profile = Profile.objects.get(user=userid)
    except ObjectDoesNotExist:
        return Response({'error': f'Profile for UserID: {userid} does not exist'}, status=status.HTTP_404_NOT_FOUND)

    user = UserRegisterSerializer(user)
    profile = ProfileSerializer(profile)

    profile = dict(profile.data, **user.data)

    # Remove profile's coordinates
    del profile['location']

    return Response(profile)


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
