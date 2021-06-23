from django.urls import path
from .views import EventView, joinEventView, recommendationView 


urlpatterns = [
    path("", EventView.as_view(), name="event-post"),
    path('<int:id>/', EventView.as_view(), name="event-get"),
    path('accept/<int:id>/', EventView.as_view(), name="accept-invite"),
    path('join/<int:id>/', joinEventView, name='join-event'),
    path('recommeded/', recommendationView, name='recommended')
]
