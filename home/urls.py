from django.urls import path
from .views import HelloView, ProfileView, PostsView


urlpatterns = [
    path("", HelloView.as_view(), name="hello"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("posts/", PostsView.as_view(), name="posts")
]
