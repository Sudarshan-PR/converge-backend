from django.contrib.gis.geos import Point
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
        data = request.data
        try:
            event = Events.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({'error': f'Event with ID: {id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user == event.host:
            return Response({'perm': 'is_permitted'})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        

    def get(self, request, id):
        event = None
        try:
            event = Events.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({'error': f'Event with ID: {id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

        event = EventGetSerializer(event)
        return Response(event.data)
