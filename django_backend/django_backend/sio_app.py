import socketio
from chat.models import Message, Chatroom
from chat.serializers import ChatroomSerializer, MessageSerializer
from account.models import User
from django.db import close_old_connections
from asgiref.sync import sync_to_async


# Create Socket.IO server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=['http://localhost:5173'])

connected_users = {
    'General': set(),
}

@sio.event
async def connect(sid, environ):
    print(f"Client {sid} connected")
   
@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")  
    
# Helper functions to fetch user, chatroom and save messages
@sync_to_async
def get_user_by_id(user_id):
    return User.objects.get(id=user_id)

@sync_to_async
def get_general_chatroom():
    return Chatroom.objects.get(name="General")

@sync_to_async
def save_message(message_body, user, chat_room):
    Message.objects.create(
        body=message_body,
        created_by=user,
        sent_to_chatroom=chat_room
    )
    
@sio.event
async def send_public_message(sid, data):
    try:   
        user_id = data['user_id']
        message_body = data['message']
        # room_name = data.get('room_name', 'General')
    
    
        user = await get_user_by_id(user_id)
        # print(f"debugging: user name = {user.name}")
        chatroom = await get_general_chatroom()
        # print(f"debugging: room name = {chatroom.name}")
        
        msg = await save_public_message(user, message_body, chatroom)
        print(f'debug (send) save_public_message. message body: {msg['body']}, created_by: {msg['created_by']}, sent_to_chatroom: {msg['sent_to_chatroom']}, created_at: {msg['created_at']}, created_at_formatted: {msg['created_at_formatted']}')
        
        # Broadcast message to the room
        print(f"Emitting message '{message_body}' from user {user_id} to room: {chatroom}")
        print(f"Rooms for client {sid}: {sio.rooms(sid)}")
        await sio.emit('chat_message', {
            'body': message_body,
            'sender': user.name,
            'created_at': msg['created_at'],
            'created_at_formatted': msg['created_at_formatted']
        }, room=chatroom.name)
        
    # except User.DoesNotExist:
    #     print(f"User with ID {user_id} does not exist.")
    except Exception as e:
        print(e)
    finally:
        close_old_connections()
        
@sio.event
def send_private_message(sid, data):
    
    sender_id = data.get('sender_id')
    recipient_id = data.get('recipient_id')
    message_body = data.get('message')
    
    try:
        sender = User.objects.get(id=sender_id)
        recipient = User.objects.get(id=recipient_id)
        
        save_private_message(sender, message_body, recipient)
        
        sio.emit('private_message', {
            'body': message_body,
            'sender': sender.name,
            'recipient': recipient.name
        }, to=recipient_id)
    except User.DoesNotExist:
        print(f"User with ID {sender_id} or {recipient_id} does not exist.")
    finally:
        close_old_connections()
        
@sio.event
async def join_room(sid, data):
    room = data.get('room', 'General')
    user_id = data.get('user_id')
    user_name = data.get('user_name')
    
    if room not in connected_users:
        connected_users[room] = set()
        
    connected_users[room].add(user_name)
    
    await sio.enter_room(sid, room)
    
    # await asyncio.to_thread(sio.enter_room, sid, room)
    
    print(f"Client {sid} joined {room}")
    print(f"Rooms for client {sid}: {sio.rooms(sid)}")
    
    await send_user_list(room)
    
    await sio.emit('chat_message', {
        'body': f'{user_name} has joined the chat.',
        'sender': 'System'
    }, room=room)
    
    await sio.emit('chat_message', {
        'body': f'Welcome to the chat { user_name }!',
        'sender': 'System',
    }, room=sid)

async def send_user_list(room):
    user_list = sorted(list(connected_users[room]))
    await sio.emit('user_list', user_list, room=room)
    
@sio.event
async def leave_room(sid, data):
    room = data.get('room_name', 'General')
    user_id = data.get('user_id')
    user_name = data.get('user_name')
    
    await sio.leave_room(sid, room)
    print(f"Client {sid} left room {room}")
    
    connected_users[room].remove(user_name)
    await send_user_list(room)
    
    await sio.emit('chat_message', {
        'body': f'{user_name} has left the chat :c',
        'sender': 'Very sad System'
    }, room=room)
    
# Helper functions for database operations
@sync_to_async
def save_public_message(sender, message_body, chatroom):
    # print(f"TEST | Saved message to database: body={message_body}, created_by={sender}, sent_to_chatroom={chatroom}")
    raw_msg = Message(body=message_body, created_by=sender, sent_to_chatroom=chatroom)
    raw_msg.save()
    
    msg = MessageSerializer(raw_msg)
    print(f'debug save_public_message. message body: {msg.data['body']}, created_by: {msg.data['created_by']}, sent_to_chatroom: {msg.data['sent_to_chatroom']}, created_at: {msg.data['created_at']}, created_at_formatted: {msg.data['created_at_formatted']}')
    return msg.data

@sync_to_async 
def save_private_message(sender, message_body, recipient):
    print(
        f"TEST | Saved message to database: body={message_body}, created_by={sender.name}, sent_to_private={recipient}"
    )