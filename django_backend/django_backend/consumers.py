import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from chat.models import Message, Chatroom
from channels.db import database_sync_to_async
from account.models import User

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = "General"
        self.room_group_name = f'chat_{self.room_name}'
        
        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        # Receive a message from WebSocket
        text_data_json = json.loads(text_data)
        message_body = text_data_json['message']
        user = self.scope['user']
        
        # Optional (private message)
        recipient_username = text_data_json.get('recipient', None)  
        recipient_uuid = text_data_json.get('recipient_uuid', None)
        
        if recipient_username:  # Private message
            recipient = await self.get_user_by_username(recipient_username)
            recipient_uuid = await self.get_user_by_uuid(recipient_uuid)
            
            if recipient:
                await self.save_private_message(message_body, user, recipient)
                await self.send_private_message(recipient, message_body, user)
        else:   # General chat
            await self.save_public_message(message_body, user)
        
            # Broadcast message to room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_body,
                    'sender': user.name
                }
            )
    
    async def chat_message(self, event):
        # Send message to WebSocket
        message = event['message']
        sender = event['sender']
        
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
    
    async def send_private_message(self, recipient, message, sender):
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender.name,
            'recipient': recipient.name
        }))
    
    @database_sync_to_async
    def save_private_message(self, message_body, sender, recipient):
        print(f'TEST (private) This is the message object to be saved: body={message_body}, created_by={sender}, sent_to_private={recipient}')
    
    @database_sync_to_async    
    def save_public_message(self, message_body, sender):
        chat_room = self.get_chatroom_by_name(self.room_name)
        
        print(f"TEST (public) This is the message object to be saved: body={message_body}, created_by={sender}, sent_to_chatroom={chat_room}")
    
    @database_sync_to_async
    def get_chatroom_by_name(self, name):
        try:
            return Chatroom.objects.get(name=name)
        except:
            return f"No chatroom named {name} found in database"
    
    @database_sync_to_async
    def get_user_by_username(self, name):
        try:
            return User.objects.get(name=name)
        except User.DoesNotExist:
            return None
    
    @database_sync_to_async
    def get_user_by_uuid(self, uuid):
        try:
            return User.objects.get(id=uuid)
        except User.DoesNotExist:
            return None
    
