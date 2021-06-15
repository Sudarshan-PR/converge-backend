from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.measure import Distance 
from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Events
from .serializers import EventCreateSerializer, EventGetSerializer, EventPatchSerializer

from register.models import User
from home.models import Profile

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

    # Partial Updates
    def patch(self, request, id):
        event = Events.objects.get(id=id)
        
        if request.user == event.host:
            data = request.data
            serializer = EventPatchSerializer(data=data)

            if serializer.is_valid():
                saved = serializer.save(id)
            
                if saved:
                    return Response({
                        'msg': 'Fields Updated.',
                        'Updated_Data': saved
                    })
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': 'You are not the host. Only Hosts can send this request.'}, status=status.HTTP_401_UNAUTHORIZED)

    # Get all events
    def get(self, request, id=0):
        # If no ID is specified
        if id == 0:
            now = timezone.localdate()

            # Default search radius
            radius = 150

            # Set readius when param is given
            if r := request.query_params.get("radius"):
                radius = int(r)
        
            # events = Events.objects.filter(event_date__gte=now).order_by('event_date')

            point = Profile.objects.get(user=request.user.id).location

            if point:
                events = Events.objects.filter(location__distance_lte=(point, Distance(km=radius)), event_date__gte=now).order_by('event_date')
            else:
                events = Events.objects.filter(event_date__gte=now).order_by('event_date')

            # If events is empty return
            if not(events):
                return Response({'msg': f'Sorry there are no upcoming events within radius of {radius}kms from {point}.'})

            # Store coordinates from models object
            host_image = []
            host_name = []
            loc = []
            for ev in events:
                host_name.append(f'{ev.host.first_name} {ev.host.last_name}')
                host_image.append(Profile.objects.get(user=ev.host).image.url)

                try:
                    loc.append({'lon': ev.location.x, 'lat': ev.location.y})
                except:
                    loc.append({})
                
            # Serialize events QuerySet object to array of dicts
            events = EventGetSerializer(events, many=True).data

            # Add event locations into each event's dict
            i = 0
            for ev in events:
                ev['host_name'] = host_name[i]
                ev['host_image'] = host_image[i]
                ev['location'] = loc[i]
                i += 1
        
        # View for a given event ID
        else:
            events = Events.objects.get(id=id)
            
            # If events is empty return
            if not(events):
                return Response({'msg': f'Sorry there is no event for that id'}, status=status.HTTP_404_NOT_FOUND)
             
            try:
                loc = {'lon': events.location.x, 'lat': events.location.y}
            except:
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
def recommendationView(request):
    radius = 50

    id = request.query_params.get("event")

    if not(eventid):
        return Response(
            {
                'msg': 'No event parameter was provided',
                'solution': 'provide event_id as "id" in url parameter. Eg: /event/recommeded?event=13',
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    point = Events.objects.get(id=id).location


    # Get all events withing 50km of given eventID's radius
    events = Events.objects.filter(location__distance_lt=(point, Distance(km=radius)), event_date__gte=now).order_by('event_date')

    loc = []
    for e in events:
        try:
            loc.append({'lon': e.location.x, 'lat': e.location.y})
        except:
            loc.append({})

    events = EventGetSerializer(events, many=True).data

    # Add event locations into each event's dict
    i = 0
    for e in events:
        e['location'] = loc[i]
        i += 1
    
    return Response(events)

# Accept Invite
# def patch(self, request, id):
    # event = Events.objects.get(id=id)
        
    # event.attendees.add(request.user)

    # event = EventGetSerializer(event)
    # return Response(event.data)