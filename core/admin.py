from django.contrib import admin
from .models import User, ChatRoom, Message, Notification

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_online', 'is_superuser')
    list_filter = ('is_online', 'is_superuser')
    search_fields = ('username', 'email')

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_group', 'admin', 'created_at')
    list_filter = ('is_group',)
    search_fields = ('name', 'admin__username')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'room', 'content_short', 'timestamp', 'is_read')
    list_filter = ('room', 'sender', 'is_read')
    search_fields = ('content', 'sender__username')
    
    def content_short(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_short.short_description = 'Content'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message_short', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('message', 'user__username')
    
    def message_short(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_short.short_description = 'Message'