# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
# import json
# from chat.core.models.user import User
# from chat.core.models.message import Message

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from event.models import Events
from home.models import Profile

from django.contrib.auth import get_user_model
User = get_user_model()

class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        room_group_names = self.get_room_group_names(self.scope['user'])
        for room in self.room_group_names:
            async_to_sync(self.channel_layer.group_discard)(room, self.channel_name)

        self.close()

    def get_room_group_names(self, user):
        events = Events.objects.filter(attendees=self.scope['user'])

        room_group_names = [] 
        for event in events: 
            room_group_names.append(f'room_{event.id}')
        
        return room_group_names

    def init(self, content):
        '''
            What it does?
                - Set user in scope and get his profile picture
                - Add channel to groups of his attending events

            Basically the initializing process before he can start sending and receiving msgs.
        '''
        try:
            user = User.objects.get(id=content['user']['_id'])

            # Set user in scope
            self.scope['user'] = user

            # Get user's profile image
            image = Profile.objects.get(user=user).image
            if image:
                self.avatar = image.url
            else:
                self.avatar = None

        except Exception as e:
            self.send_json({'error': str(e)})
        
        self.room_group_names = self.get_room_group_names(user)

        # If no groups then return
        if not(self.room_group_names):
            self.send_json({'error': 'Not attending any events'})
            return

        for room in self.room_group_names:
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                room,
                self.channel_name
            )

        self.send_json({'msg': f'Done Init at rooms: {str(self.room_group_names)}'})
        
    def new_message(self, content):
        '''
            Send the new message to group
        '''
        # Populate content with user's name and profile picture
        content['user']['name'] = f'{self.scope["user"].first_name} {self.scope["user"].last_name}'
        content['user']['avatar'] = self.avatar

        # Send content to group
        async_to_sync(self.channel_layer.group_send)(
            content['to'],
            {
                'type': 'chat.message',
                'message': content
            }
        )

    def retrieve_messages(self):
        pass

    def chat_message(self, event):
        '''
            Send message to sockets
        '''
        message = event['message']

        # Send message to WebSocket
        self.send_json(message)

    commands = {
        'init': init,
        'new_message': new_message,
        'retrieve_messages': retrieve_messages,
    }
    def receive_json(self, content):
        """
            Called when msg is received through the websocket.
            content parameter is the decoded json body.
        """
        
        self.commands[content['command']](self, content)

# class ChatConsumer(WebsocketConsumer):
#     def init_chat(self, data):
#         username = data['username']
#         user, created = User.objects.get_or_create(username=username)
#         content = {
#             'command': 'init_chat'
#         }
#         if not user:
#             content['error'] = 'Unable to get or create User with username: ' + username
#             self.send_message(content)
#         content['success'] = 'Chatting in with success with username: ' + username
#         self.send_message(content)

#     def fetch_messages(self, data):
#         messages = Message.last_50_messages()
#         content = {
#             'command': 'messages',
#             'messages': self.messages_to_json(messages)
#         }
#         self.send_message(content)

#     def new_message(self, data):
#         author = data['from']
#         text = data['text']
#         author_user, created = User.objects.get_or_create(username=author)
#         message = Message.objects.create(author=author_user, content=text)
#         content = {
#             'command': 'new_message',
#             'message': self.message_to_json(message)
#         }
#         self.send_chat_message(content)

#     def messages_to_json(self, messages):
#         result = []
#         for message in messages:
#             result.append(self.message_to_json(message))
#         return result

#     def message_to_json(self, message):
#         return {
#             'id': str(message.id),
#             'author': message.author.username,
#             'content': message.content,
#             'created_at': str(message.created_at)
#         }

#     commands = {
#         'init_chat': init_chat,
#         'fetch_messages': fetch_messages,
#         'new_message': new_message
#     }

#     def connect(self):
#         self.room_name = 'room'
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#         self.accept()

#     def disconnect(self, close_code):
#         # leave group room
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     def receive(self, text_data):
#         data = json.loads(text_data)
#         self.commands[data['command']](self, data)

#     def send_message(self, message):
#         self.send(text_data=json.dumps(message))

#     def send_chat_message(self, message):
#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         message = event['message']
#         # Send message to WebSocket
#         self.send(text_data=json.dumps(message))