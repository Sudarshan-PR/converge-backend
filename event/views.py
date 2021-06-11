from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance 
from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Events
from .serializers import EventCreateSerializer, EventGetSerializer

from register.models import User

class EventView(APIView):
    permisson_classes = (IsAuthenticated,)

    # Create new event
    def post(self, request):
        data = request.data

        serializer = EventCreateSerializer(data=data)
       
        if serializer.is_valid():
            serializer.save(host=request.user)
            
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Update event
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

    # Accept Invite
    def patch(self, request, id):
        event = Events.objects.get(id=id)
            
        event.attendees.add(request.user)

        event = EventGetSerializer(event)
        return Response(event.data)
        
    # Get all events
    def get(self, request, id=0):
        # If no ID is specified
        if id == 0:
            now = timezone.localdate()
            # events = Events.objects.filter(event_date__gte=now).order_by('event_date')

            radius = 100
            point = Profile.filter.get(user=request.user).location   
            events = Events.objects.filter(location__distance_lt=(point, Distance(km=radius)), event_date__gte=now).order_by('event_date')

            # If events is empty return
            if not(events):
                return Response({'msg': f'Sorry there are no upcoming events.'})

            loc = []
            for e in events:
                try:
                    loc.append({'lon': e.location.x 'lat': e.location.y})
                except:
                    loc.append({})
                
            events = EventGetSerializer(events, many=True)

            events = events.data

            # Add event locations into each event's dict
            i = 0
            for e in events:
                e['location'] = loc[i]
                i += 1
        
        # View for a given event ID
        else:
            events = Events.objects.get(id=id)
            
            # If events is empty return
            if not(events):
                return Response({'msg': f'Sorry there is no event for that id'}, status=status.HTTP_404_NOT_FOUND)
             
            try:
                loc = {'lat': events.location.y, 'lon': events.location.x}
            except Exception as e:
                loc = {}

            events = EventGetSerializer(events)
            events = events.data

            events['location'] = loc

        return Response(events)

@api_view(['POST'])
def inviteView(request, id):
    userid = request.data['userid']
    # return Response({'eventid': id, 'userid': userid})

    event = Events.objects.get(id=id)

    # Check if host sent the request
    if request.user == event.host:
        user = User.objects.get(id=userid)    
        event.invites_sent.add(request.user)

        return Response({'msg': "Successfully invited"})

    return Response({'msg': "Action Not Allowed. You are not the host."}, status=status.HTTP_401_UNAUTHORIZED)

    event = EventGetSerializer(event)
    return Response(event.data)


@api_view(['GET'])
def getRecommendation(request, id):
    