from django.utils import timezone
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
from event.serializers import PendingRequestsSerializer, EventGetSerializer, EventProfileSerializer
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
        
        join_requests = Events.objects.filter(invites=request.user.id)

        if join_requests:
            pending_requests = PendingRequestsSerializer(join_requests, many=True)
            events = pending_requests.data
            pending_requests = []

            for ev in events:
                pending_requests.append({
                    'id'    :   ev['id'],
                    'title' :   ev['title'],
                    'image' :   ev['image'],
                    'addr'  :   ev['addr'],
                })

            profile['pending_requests'] = pending_requests

        else:
            profile['pending_requests'] = []
        
        now = timezone.localdate()
        hosted_events = Events.objects.filter(event_date__gte=now, host=request.user).order_by('event_date')
        if hosted_events:
            hosted_events_serializer = EventGetSerializer(hosted_events, many=True)
            data = hosted_events_serializer.data

            for ev,d in zip(hosted_events,data):
                invites_quarySet = ev.invites.all()
                if invites_quarySet:
                    invites = []
                    for user in invites_quarySet:
                        try:
                            image = Profile.objects.get(user=user).image.url
                        except:
                            image = None

                        invites.append({
                            'userid': user.id,
                            'image': image,
                            'name': f'{user.first_name} {user.last_name}'
                        })
                    
                    d['invites'] = invites
            

            profile['hosted_events'] = data
        
        else:
            profile['hosted_events'] = None

        attending_events = Events.objects.filter(attendees=request.user)
        if attending_events:
            event_serializer = EventProfileSerializer(attending_events, many=True)

            profile['attending_events'] = event_serializer.data
        else:
            profile['attending_events'] = None

        return Response(profile)

@api_view()
def get_user_profile(request, userid):
    user, profile = None, None
    try:
        user = User.objects.get(id=userid)
        profile = Profile.objects.get(user=userid)
    except ObjectDoesNotExist:
        return Response({'error': f'Profile for UserID: {userid} does not exist'}, status=status.HTTP_404_NOT_FOUND)

    user_serializer = UserRegisterSerializer(user)
    profile = ProfileSerializer(profile)

    profile = dict(profile.data, **user_serializer.data)
    
    # Events the user has hosted
    now = timezone.now()
    hosted_events = Events.objects.filter(event_date__gte=now, host=user).order_by('event_date')
    if hosted_events:
        hosted_events_serializer = EventGetSerializer(hosted_events, many=True)
        profile['hosted_events'] = hosted_events_serializer.data
    else:
        profile['hosted_events'] = None

    # Events the user is attending
    attending_events = Events.objects.filter(attendees=user)
    if attending_events:
        event_serializer = EventProfileSerializer(attending_events, many=True)

        profile['attending_events'] = event_serializer.data
    else:
        profile['attending_events'] = None

    # Remove profile's coordinates
    del profile['location']

    return Response(profile)


class PostsView(APIView):
    def get(self, request):
        posts = Posts.objects.all().order_by('created_date')
        post_data = PostSerializer(posts, many=True).data

        return Response(post_data)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            post = serializer.save(user=request.user)
            post_serializer = PostSerializer(post)

            return Response(post_serializer.data)

        return Response(serializer.errors)