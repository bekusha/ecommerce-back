import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
import logging
import asyncio

logger = logging.getLogger(__name__)

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.device_id = self.scope['url_route']['kwargs'].get('device_id', None)  # უსაფრთხო მიღება
        if not self.device_id:
            print(f"Device ID is missing for user {self.user_id}")
        self.room_group_name = f"user_{self.user_id}_{self.device_id}"




        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        logger.info("f User {self.scope['user']} connected to WebSocket")
        await self.accept()
        asyncio.create_task(self.send_ping_messages())

    async def disconnect(self, close_code):
        print(f"WebSocket disconnected for user {self.user_id}")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"Received WebSocket message: {data}")

        if data['type'] == 'new_order':
            # Send confirmation or broadcast update
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'order_update',
                    'order_id': data['order_id'],
                    'status': 'Processing',
                }
            )

    async def order_update(self, event):
         await self.send(text_data=json.dumps({
        'type': 'order_update',
        'order_id': event.get('order_id'),
        'status': event.get('status'),
        'order_type': event.get('order_type'),
        'phone': event.get('phone'),
        'address': event.get('address'),
        'email': event.get('email', ''),  # Default to empty string if None
        'courier_name': event.get('courier_name', ''),  # Default to empty string if None
        'courier_phone': event.get('courier_phone', ''),
        'delivery_time': str(event.get('delivery_time', '')),  # Convert datetime to string
    }))


async def send_ping_messages(self):
        """Periodically sends ping messages to check connection"""
        while True:
            await asyncio.sleep(30)  # Send ping every 30 seconds
            try:
                await self.send(text_data=json.dumps({'type': 'ping'}))
                logger.info(f"Ping sent to user {self.user_id}")
            except Exception as e:
                logger.error(f"Failed to send ping to user {self.user_id}: {e}")
                break  # Stop sending pings if the connection is broken