from django.urls import path
from .views import EventView #, accept_invite


urlpatterns = [
    path("", EventView.as_view(), name="event-post"),
    path('<int:id>/', EventView.as_view(), name="event-get"),
    path('accept/<int:id>/', EventView.as_view(), name="accept-invite")
]
