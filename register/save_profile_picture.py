import home.models
import tempfile
from django.core import files

def save_profile(backend, user, response, is_new=False, *args, **kwargs):
    if backend.name == 'google-oauth2':
        if is_new and response.get('picture'):
            image = requests.get(response['picture'], stream=True)
            
            # Create a temporary file
            tf = tempfile.NamedTemporaryFile()

            # Read the streamed image in sections
            for block in image.iter_content(1024 * 8):
                
                # If no more file then stop
                if not block:
                    break

                # Write image block to temporary file
                tf.write(block)

            # Create the model you want to save the image to
            profile = home.models.Profile.objects.get(user=user)

            profile.image = files.File(tf)
            profile.save()
