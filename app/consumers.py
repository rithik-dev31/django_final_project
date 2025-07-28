from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from .models import ChatMessage, Section, UserProfile  # ✅ Changed import
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
        username = data['username']
        message = data['message']

        section_id = self.scope['url_route']['kwargs'].get('section_id')
        if not section_id:
            print("No section_id in scope")
            return

        print(f"Received message for section {section_id}: {message} from {username}")
        username = username.strip()
        print("Calling save_message...")

        await self.save_message(section_id, username, message)

        await self.channel_layer.group_send(
            f'chat_{section_id}',
            {
                'type': 'chat_message',
                'username': username,
                'message': message
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'username': event['username'],
            'message': event['message']
        }))

    @sync_to_async
    def save_message(self, section_id, username, message):
        section = Section.objects.get(id=section_id)

        try:
            user = UserProfile.objects.get(username=username)  # ✅ Changed to UserProfile
        except UserProfile.DoesNotExist:
            user = None  # Handle as needed

        ChatMessage.objects.create(
            section=section,
            user=user,
            message=message,
        )
