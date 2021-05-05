from django.contrib.gis.geos import Point

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class EventView(APIView):
    permisson_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data

        serializer = ProfileSerializer(data=data)
       
        if serializer.is_valid():
            profile = serializer.save(request.user.id)
            
            profile = ProfileSerializer(profile)

            msg = {'msg': 'Profile has been updated!','user': request.user.id}
            resp = dict(profile.data, **msg)
            
            return Response(resp)

        return Response(serializer.errors)

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
            loc = [profile.location.x, profile.location.y]
        except Exception as e:
            loc = str(e)

        profile = ProfileSerializer(profile)
        user = UserRegisterSerializer(request.user)

        # Test if profile image exists
        # try:
        #     image = profile.image.url
        # except:
        #     image = None

        profile = dict(profile.data, **user.data)
        profile['location'] = loc 

        return Response(profile)

