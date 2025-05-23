from django.db import models
from django.contrib.auth.models import User
import shortuuid
# Models.py
class ChatGroup(models.Model):
  group_name=models.CharField(max_length=128, unique=True,default=shortuuid.uuid)
  groupchat_name = models.CharField(max_length=128, null=True, blank=True)
  admin = models.ForeignKey(User, related_name='groupchats', blank=True, null=True, on_delete=models.SET_NULL)
  users_online = models.ManyToManyField(User, related_name='online_in_groups',blank=True)
  members = models.ManyToManyField(User, related_name='chat_groups', blank=True)
  is_private = models.BooleanField(default=False)

  def _str_(self):
    return self.group_name

class GroupMessage(models.Model):
  group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='chat_messages')
  author=models.ForeignKey(User, on_delete=models.CASCADE)
  body=models.CharField(max_length=300)
  created=models.DateTimeField(auto_now_add=True)

  def _str_(self):
    return f'{self.author.username} : {self.body}'


  class Meta:
    ordering = ['-created']


