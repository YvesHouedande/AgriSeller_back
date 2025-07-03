import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            token = self.scope['query_string'].decode().split('=')[1]
            user = await self.get_user_from_token(token)
            
            if user is None or user.is_anonymous:
                await self.close()
            else:
                self.user = user
                self.room_group_name = f"user_{user.id}"
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
                await self.accept()
        except Exception as e:
            await self.close()

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            from django.contrib.auth import get_user_model
            User = get_user_model()
            return User.objects.get(id=user_id)
        except Exception:
            return AnonymousUser()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event["content"]))