from .models import Chatroom, Message

from account.serializers import UserSerializer

from rest_framework import serializers

class ChatroomSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True)
    
    class Meta:
        model = Chatroom
        fields = ('id', 'name', 'users')
        
class MessageSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    sent_to_private = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ('id', 'body', 'created_by', 'created_at', 'sent_to_chatroom', 'sent_to_private', 'created_at_formatted')