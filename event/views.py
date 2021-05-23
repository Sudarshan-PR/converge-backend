from django.contrib.gis.geos import Point
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Events
from .serializers import EventCreateSerializer, EventGetSerializer


class EventView(APIView):
    permisson_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data

        serializer = EventCreateSerializer(data=data)
       
        if serializer.is_valid():
            serializer.save(host=request.user)
            
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def patch(self, request, id):
        event = Events.objects.get(id=id)
            
        event.attendees.add(request.user)

        event = EventGetSerializer(event)
        return Response(event.data)
        
    def get(self, request):
        now = timezone.localdate()

        events = Events.objects.filter(event_date__gte=now).order_by('event_date')

        # If events is empty return
        if not(events):
            return Response({'msg': f'Sorry there are no upcoming events.'})

        events = EventGetSerializer(events, many=True)
        return Response(events.data)

# @api_view()
# def accept_invite(request, id):