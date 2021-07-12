import logging

from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
) 
from requests.exceptions import ConnectionError, HTTPError

logger = logging.getLogger('debug_logger')

# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.
def send_push_message(token, title, message, extra=None):
    try:
        response = PushClient().publish(
            PushMessage(
                to=token,
                title= title,
                body=message,
                data=extra
            ))
    except PushServerError as exc:
        # Encountered some likely formatting/validation error.
        logger.debug(str({
                'token': token,
                'message': message,
                'extra': extra,
                'errors': exc.errors,
                'response_data': exc.response_data,
            }))
        raise
    except (ConnectionError, HTTPError) as exc:
        # Encountered some Connection or HTTP error - retry a few times in
        # case it is transient.
        logger.debug(str({'token': token, 'message': message, 'extra': extra}))
        raise self.retry(exc=exc)

    try:
        # We got a response back, but we don't know whether it's an error yet.
        # This call raises errors so we can handle them with normal exception
        # flows.
        response.validate_response()
    except DeviceNotRegisteredError:
        # Mark the push token as inactive
        from notifications.models import PushToken
        PushToken.objects.filter(token=token).update(active=False)
    except PushTicketError as exc:
        # Encountered some other per-notification error.
        logger.debug({
            'token': token,
            'message': message,
            'extra': extra,
            'push_response': exc.push_response._asdict(),
        })
        raise self.retry(exc=exc)