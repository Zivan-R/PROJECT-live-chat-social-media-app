import uuid
from django.db import models

from account.models import User

# Create your models here.
class Chatroom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name='chat_rooms')
    
    def __str__(self):
        return self.name

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    
    created_by = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    sent_to_private = models.ForeignKey(User, null=True, blank=True, related_name='private_messages', on_delete=models.CASCADE)
    sent_to_chatroom = models.ForeignKey(Chatroom, null=True, blank=True, related_name='public_messages', on_delete=models.CASCADE)
    
    def __str__(self):
        if self.sent_to_private:
            return f"Private message from {self.created_by.name} to {self.sent_to_private.name}: {self.body}"
        elif self.sent_to_chatroom:
            return f"Message from {self.created_by.name} in {self.sent_to_chatroom.name}: {self.body}"
        return "Message without anyone to send it to."