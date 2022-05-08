import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        self.group_name = f'notification_{user.job}'

        # join group
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        # leave group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive message from websocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        event = {
            'type': 'send_message',
            'message': message
        }

        await self.channel_layer.group_send(self.group_name, event)

    # Receieve message from group
    async def send_message(self, event):
        message = event['message']

        # send message to websocket
        await self.send(text_data=json.dumps({'message': message}))
