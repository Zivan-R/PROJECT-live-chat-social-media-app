import uuid

from django.db import models
from django.utils.timesince import timesince    # To get the "x minutes ago" format

from account.models import User # Import the custom User, not the default one by Django

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField(blank=True, null=True)
    
    # class Meta:
    #     ordering = ('created_at',)
    
    def created_at_formatted(self):
        return timesince(self.created_at)

class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to="post_attachments")
    created_by = models.ForeignKey(User, related_name='post_attachments', on_delete=models.CASCADE)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)  # blank and null will make it not required
    
    attachments = models.ManyToManyField(PostAttachment, blank=True)     # maybe one to many is better, how to do that?
    
    likes = models.ManyToManyField(Like, blank=True)
    likes_count = models.IntegerField(default=0)
    
    comments = models.ManyToManyField(Comment, blank=True)
    comments_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)    # On delete of user, will delete posts
    
    # Change ordering (newer posts appear first)
    class Meta:
        ordering = ("-created_at",)
    
    # To get the "x minutes ago" format
    def created_at_formatted(self):
        return timesince(self.created_at)