from PIL import Image
import requests

def save_profile(backend, user, response, is_new=False, *args, **kwargs):
    if backend.name == 'google-oauth2':
        if is_new and response.get('picture'):
            image = requests.get(requests['picture'], stream=True).raw
            img = Image.open(image)
            Profile.objects.filter(owner=user).update(image=img)
