from django.urls import path
from .views import HelloView, ProfileView, PostsView, get_user_profile


urlpatterns = [
    path("", HelloView.as_view(), name="hello"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/<int:userid>/", get_user_profile, name="user_profile"),
    path("posts/", PostsView.as_view(), name="posts")
]
