import home.models
from django.core import files

import tempfile
import requests
import logging

logger = logging.getLogger(__name__)

def save_profile(backend, user, response, is_new=False, *args, **kwargs):
    logger.info('Inside pipeline')
    if backend.name == 'google-oauth2':
        logger.info('Inside google-oauth2')

        if response.get('picture'):
            logger.info('Inside response')

            image = requests.get(response['picture'], stream=True)
            logger.info("Image: " + str(type(image)))
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
            
            logger.info('Profile:' + profile.__str__())
            profile.image = files.File(tf)
            profile.save()