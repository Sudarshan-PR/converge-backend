import home.models
from PIL import Image
import requests

def save_profile(backend, user, response, is_new=False, *args, **kwargs):
    if backend.name == 'google-oauth2':
        if is_new and response.get('picture'):
            image = requests.get(response['picture'], stream=True).raw
            img = Image.open(image)
            home.models.Profile.objects.get(user=user).update(image=img)
