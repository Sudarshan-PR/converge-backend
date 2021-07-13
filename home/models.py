from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.gis.geos import Point

from django.contrib.auth import get_user_model
User = get_user_model()

from event.models import Events 

import logging

logger = logging.getLogger('debug_logger')

# Posts Model
class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, auto_now=True, auto_now_add=False)
    caption = models.CharField(max_length=30)
    tags = ArrayField(models.CharField(max_length=15), blank=True, null=True)

    def __str__(self):
        return f'{self.user} : {self.caption}'
            

# User Profile Model
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True)
    tags = ArrayField(models.CharField(max_length=15), blank=True, null=True)
    bio = models.TextField(max_length=100, blank=True)
    dob = models.DateField(blank=True, null=True, auto_now=False, auto_now_add=False)
    location = models.PointField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.email} : {self.first_name}'


#
# Update profile picture on social login
#
# from social_core.backends import google
# from social_django.signals import socialauth_registereo
# def new_users_handler(sender, user, response, details, **kwargs):
#     user.is_new = True
#     if user.is_new:
#         if "id" in response:
            
#             from urllib2 import urlopen, HTTPError
#             from django.template.defaultfilters import slugify
#             from django.core.files.base import ContentFile
            
#             try:
#                 if sender == google.GoogleOAuth2Backend and "picture" in response:
#                     url = response["picture"]
    
#                 if url:
#                     avatar = urlopen(url)
#                     profile = Profile.objects.get(user=user)
                    
#                     logger.debug(f'Profile: {profile.__str__()} \n Image URL: {url}')

#                     profile.image.save(slugify(user.username + " social") + '.jpg', ContentFile(avatar.read()))              
                                    
#                     profile.save()
    
#             except HTTPError:
#                 pass

#     return False

# socialauth_registered.connect(new_users_handler, sender=None)