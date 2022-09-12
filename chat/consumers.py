import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from accounts.models import User
from accounts.serializers import UserSerializer
from chat.models import ChatLog, ChatRoom

from django.shortcuts import get_object_or_404


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['content']

        user = self.scope['user']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'content': message,
                'user_id': user.id
            }
        )

        # create chatlog
        await self.create_chatlog(message)

    async def chat_message(self, event):
        message = event['content']
        user_id = event['user_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'content': message,
            'user': UserSerializer(await self.get_user(user_id)).data
        }))

    @database_sync_to_async
    def create_chatlog(self, message):
        ChatLog.objects.create(
            room=ChatRoom.objects.get(room_name=self.room_name),
            user=get_object_or_404(User, id=self.scope['user'].id),
            content=message
        )

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)
