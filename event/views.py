import logging
from stream_chat import StreamChat

from django.contrib.gis.geos import Point, GEOSGeometry
from django.contrib.gis.measure import Distance 
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Events
from .serializers import EventCreateSerializer, EventGetSerializer, EventPatchSerializer, EventAcceptSerializer

from register.models import User
from home.models import Profile

from notification.utils import send_push_message
from notification.models import ExpoToken

logger = logging.getLogger('debug_logger')

chatClient = StreamChat(api_key=settings.STREAM_API_KEY, api_secret=settings.STREAM_SECRET_KEY)

class EventView(APIView):
    permisson_classes = (IsAuthenticated,)


    # Create new event
    def post(self, request):
        data = request.data

        serializer = EventCreateSerializer(data=data)
       
        if serializer.is_valid():
            event = serializer.save(host=request.user)
            if(event):
                event_data = EventGetSerializer(event).data

                # Create chat channel when event is created
                channel = chatClient.channel("messaging", f'{event_data["id"]}')
                channel.create(f'{event_data["host"]}')
                channel.update({
                    "name": f"{event_data['title']}",
                })
                channel.add_moderators([str(event_data['host'])])

                return Response(event_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Partial Updates
    def patch(self, request, id):
        event = Events.objects.get(id=id)
        
        if request.user == event.host:
            data = request.data
            serializer = EventPatchSerializer(data=data)

            if serializer.is_valid():
                event = serializer.save(id)
            
                if event:
                    event_data = EventGetSerializer(event).data

                    # Update chat channel details when updated event
                    channel = chatClient.channel("messaging", f'{event_data["id"]}')
                    if event_data['image']:
                        channel.update({
                            "name": f"{event_data['title']}",
                            "image": f"{event_data['image']}",
                        })
                    else:
                        channel.update({
                            "name": f"{event_data['name']}"
                        })
    
                    return Response({
                        'msg': 'Fields Updated.',
                        'event': event_data
                    })
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': 'You are not the host. Only Hosts can send this request.'}, status=status.HTTP_401_UNAUTHORIZED)

    # Get all events
    def get(self, request, id=False):
        # If no ID is specified return all available events
        if not(id):
            now = timezone.localdate()

            # Default search radius
            radius = False
            interests = False

            # Set readius when param is given
            if r := request.query_params.get("radius"):
                radius = int(r)

            # Set interest when param is given
            if i := request.query_params.get("interest"):
                if i == "true":
                    interests = Profile.objects.get(user=request.user).tags
        
            point = Profile.objects.get(user=request.user.id).location

            # 
            if point and interests and radius:
                events = Events.objects.filter(location__distance_lte=(point, Distance(km=radius)), event_date__gte=now, tags__contains=interests).exclude(host=request.user).order_by('event_date')
            elif interests:
                events = Events.objects.filter(event_date__gte=now, tags__contains=interests).exclude(host=request.user).order_by('event_date')
            elif interests and radius and point:
                events = Events.objects.filter(location__distance_lte=(point, Distance(km=radius)), event_date__gte=now, tags__contains=interests).exclude(host=request.user).order_by('event_date')
            elif point and radius:
                events = Events.objects.filter(location__distance_lte=(point, Distance(km=radius)), event_date__gte=now).exclude(host=request.user).order_by('event_date')
            else:
                events = Events.objects.filter(event_date__gte=now).exclude(host=request.user).order_by('event_date')

            # If events is empty return
            if not(events):
                return Response({'msg': f'Sorry there are no upcoming events within radius of {radius}kms from {point}. Interets:{interests}'})

            # Store coordinates from models object
            loc = []

            host_image = []
            host_name = []

            join_requests = Events.objects.filter(invites=request.user.id) # All events user requested to join
            requested = []

            for ev in events:
                host_name.append(f'{ev.host.first_name} {ev.host.last_name}')

                try:
                    host_image.append(Profile.objects.get(user=ev.host).image.url)
                except:
                    host_image.append(None)

                try:
                    loc.append({'lon': ev.location.x, 'lat': ev.location.y})
                except:
                    loc.append(None)
                
                # If user already requested to join the event appened True else False
                if ev in join_requests:
                    requested.append(True)
                else:
                    requested.append(False)
                
            # Serialize events QuerySet object to array of dicts
            events = EventGetSerializer(events, many=True).data
            
            user = request.user.id
            # Add event locations into each event's dict
            i = 0
            for ev in events:
                ev['host_name'] = host_name[i]
                ev['host_image'] = host_image[i]
                ev['location'] = loc[i]
                ev['requested'] = requested[i]

                # If not host delete invites from
                if ev['host'] is not request.user.id:
                    del ev['invites']

                i += 1
        
        # View for a given event ID
        else:
            try:
                events = Events.objects.get(id=id)
            except ObjectDoesNotExist:
                return Response({'msg': f'Event for id: {id} Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                loc = {'lon': events.location.x, 'lat': events.location.y}
            except:
                loc = {}

            # All join requests sent by user
            join_requests = Events.objects.filter(invites=request.user.id)
            
            if events in join_requests:
                requested = True
            else:
                requested = False

            events = EventGetSerializer(events)
            events = events.data

            events['requested'] = requested
            events['location'] = loc

            if events['host'] is not request.user.id:
                del events['invites']
            else:
                i = 0
                for invite in events['invites']:
                    user = User.objects.get(id=invite)
                    try:
                        image = Profile.objects.get(user=user).image.url
                    except:
                        image = None

                    events['invites'][i] = {
                        'userid': user.id,
                        'name': f'{user.first_name} {user.last_name}',
                        'image': image
                    }
                    i += 1

        return Response(events)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def joinEventView(request, id):
    user = request.user
    event = Events.objects.get(id=id)

    try:
        event.invites.add(user)
        
        # Send notification to event host
        tokens = ExpoToken.objects.filter(user=event.host, active=True)
        title = 'Event'
        message = f'{user.first_name} {user.last_name} has requested to join {event.title}.'
        for token in tokens:
            send_push_message(token.token, title=title, message=message)

        return Response({'msg': "Successfully sent request to join the event."})

    except Exception as e:
        return Response({'msg': f'Caught an exception. {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

    event = EventGetSerializer(event)
    return Response(event.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendationView(request):
    id = request.query_params.get("event")

    if not(id):
        return Response(
            {
                'msg': 'No event parameter was provided',
                'solution': 'provide event_id as "id" in url parameter. Eg: /event/recommeded?event=13',
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    now = timezone.localdate()

    radius = request.query_params.get("radius")
    # If radius not set, default radius
    if not(radius):
        radius = 50

    # Get event's location
    try: 
        point = Events.objects.get(id=id).location
    except ObjectDoesNotExist:
        return Response({'msg': 'Provided event ID is invalid. No events exist for the given ID.'}, status=status.HTTP_400_BAD_REQUEST)

    # Get all events withing 50km of given eventID's radius
    events = Events.objects.filter(location__distance_lt=(point, Distance(km=radius)), event_date__gte=now).exclude(id=id).order_by('event_date')

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

# Attendings events
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attending_events(request):
    events = Events.objects.filter(attendees=request.user)
    pass


# Accept Invite
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_invite(request, id):
    event = Events.objects.get(id=id)
       
    if event.host == request.user:
        serializer = EventAcceptSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            user = User.objects.get(id=data['userid'])
            event.attendees.add(user)
            event.invites.remove(user)

            # Add user to event's group chat
            channel = chatClient.channel("messaging", f'{event.id}')
            channel.add_members([f'{user.id}'])

            # Send notification to user that he got accepted
            tokens = ExpoToken.objects.filter(user=user, active=True)
            title = 'Event'
            message = f'Your request to join {event.title} has been accepted.'
            for token in tokens:
                send_push_message(token.token, title=title, message=message)

            return Response({'msg': 'Join request accepted. User is now put into the attendees list.'}, status=status.HTTP_201_CREATED)

        else:
            return Response({'msg': 'Data provided was not valid. Make sure to send "user":id <int> in json or form data'}, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response({'msg': 'You are not the host. Only Hosts can send this request.'}, status=status.HTTP_401_UNAUTHORIZED)


# Reject an invite
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_invite(request, id):
    event = Events.objects.get(id=id)
       
    if event.host == request.user:
        serializer = EventAcceptSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            user = User.objects.get(id=data['userid'])
            event.invites.remove(user)

            # Send notification to user that he got accepted
            tokens = ExpoToken.objects.filter(user=user, active=True)
            title = 'Event'
            message = f'Your request to join {event.title} has been rejected.'
            for token in tokens:
                send_push_message(token.token, title=title, message=message)

            return Response({'msg': 'Join request has been rejected. User is now removed from invites list.'}, status=status.HTTP_201_CREATED)

        else:
            return Response({'msg': 'Data provided was not valid. Make sure to send "user":id <int> in json or form data'}, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response({'msg': 'You are not the host. Only Hosts can send this request.'}, status=status.HTTP_401_UNAUTHORIZED)