from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from .models import ChatMessage, Section, UserProfile
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        logger.info(f'scope contents: {self.scope}')
        url_route = self.scope.get('url_route', {})
        kwargs = url_route.get('kwargs', {})
        logger.info(f'kwargs: {kwargs}')
        section_id = kwargs.get('section_id')

        if not section_id:
            logger.error("Section ID not found in URL route kwargs.")
            await self.close()
            return

        self.section_id = section_id
        self.group_name = f'chat_{self.section_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        username = data.get('username')
        message = data.get('message')

        section_id = self.scope['url_route']['kwargs'].get('section_id')
        if not section_id:
            logger.error("No section_id in scope")
            return

        logger.info(f"Received message for section {section_id}: {message} from {username}")
        username = username.strip()

        # Save the message and get the timestamp
        timestamp = await self.save_message(section_id, username, message)

        # Broadcast to group with timestamp
        await self.channel_layer.group_send(
            f'chat_{section_id}',
            {
                'type': 'chat_message',
                'username': username,
                'message': message,
                'timestamp': timestamp,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'username': event['username'],
            'message': event['message'],
            'timestamp': event['timestamp'],
        }))

    @sync_to_async
    def save_message(self, section_id, username, message):
        try:
            section = Section.objects.get(id=section_id)
            user = UserProfile.objects.get(username=username)
            msg = ChatMessage.objects.create(
                section=section,
                user=user,
                message=message,
            )
            # Return formatted timestamp
            return msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
