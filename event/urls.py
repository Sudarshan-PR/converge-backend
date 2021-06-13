from django.urls import path
from .views import EventView, inviteView, recommendationView 


urlpatterns = [
    path("", EventView.as_view(), name="event-post"),
    path('<int:id>/', EventView.as_view(), name="event-get"),
    path('accept/<int:id>/', EventView.as_view(), name="accept-invite"),
    path('invite/<int:id>/', inviteView, name='invite-user'),
    path('recommeded/', recommendationView, name='recommended')
]
