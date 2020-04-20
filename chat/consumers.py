from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message,Userimage,Profile
from django.shortcuts import get_object_or_404
from channels.db import database_sync_to_async
from django.template.loader import render_to_string

User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message.last_10_messages()
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        message = Message.objects.create(
            author=author_user, 
            content=data['message'])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        user = self.scope['user']
        print("user add   "+user.username)
        if user.is_authenticated:
            if user.profile.status_up==True:
                self.update_user_status(user,True,True)
            self.send_status()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        user = self.scope['user']
        print("user remove   "+user.username)
        if user.is_authenticated:
            self.update_user_statuss(user,False)
            self.send_status()

    def receive(self, text_data):
        data = json.loads(text_data)
        if data['command']=='fetch_image':
            author=data['author'];
            user=get_object_or_404(User,username=author)

            content = {
            'command': 'fetch_image',
            'image': str(user.person.image.url)
            }
            self.send(text_data=json.dumps(content))
        elif data['command']=='change_status':
            user = self.scope['user']
            st_type=data['status_type']
            if user.is_authenticated:
                if st_type=='Online':
                    self.update_user_status(user,True,True)
                else:
                    self.update_user_status(user,False,False)
                self.send_status()
            
        else:
            self.commands[data['command']](self, data)
        

    def send_chat_message(self, message):    
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))




    def update_user_status(self, user,status,status_up):
        return Profile.objects.filter(user_id=user.pk).update(status=status,status_up=status_up)
    def update_user_statuss(self, user,status):
        st_ch=get_object_or_404(Profile,user_id=user.pk)
        if st_ch.status_up==False:
            print("11111111111111111111111111")
            return Profile.objects.filter(user_id=user.pk).update(status=status)
        else:
            print("2222222222222222222222222")
            return Profile.objects.filter(user_id=user.pk).update(status=status,status_up=True)

    def send_status(self):
        users = User.objects.all()
        html_users = render_to_string("chat/sidebar.html",{'users':users})
        content = {
            'command': 'status',
            'html_users': html_users
        }
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'user_update',
                "event": "Change Status",
                "html_users": content
            }
        )  

    def user_update(self,event):
        self.send(text_data=json.dumps(event['html_users']))



