from django.contrib.gis import admin
from .models import Events 

admin.site.register(Events, admin.GeoModelAdmin)