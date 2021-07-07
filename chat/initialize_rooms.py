from stream_chat import StreamChat

from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

from event.models import Events
from .serializers import UserSerializer, EventRoomSerializer

User = get_user_model()

def initialize_rooms(client):
    now = timezone.now()
    users = UserSerializer(User.objects.all(), many=True)

    # Convert ID from int to str
    users = [{'id': str(u['id'])} for u in users.data]

    # Register all users in db
    client.update_users(users)

    # Get all events and register them
    events = Events.objects.filter(event_date__gte=now)
    events_serializer = EventRoomSerializer(events, many=True)
    for ev in events_serializer.data:
        channel = client.channel("messaging", f'{ev["id"]}')
        channel.create(str(ev['host']))
        channel.update({
            "name": f"{ev['title']}",
            "image": f"{ev['image']}",
        })

        if ev['attendees']:
            # Convert attendees id's to string
            attendees = [str(x) for x in ev['attendees']]
            channel.add_members(attendees)
        
        # Set host as channel moderator
        channel.add_moderators([str(ev['host'])])