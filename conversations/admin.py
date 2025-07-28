# conversations/admin.py
from django.contrib import admin
from .models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'status', 'duration_seconds', 
                   'xp_earned', 'started_at']
    list_filter = ['status', 'started_at']
    search_fields = ['user__username', 'title']
    readonly_fields = ['started_at', 'completed_at']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'message_type', 'original_text', 'timestamp']
    list_filter = ['message_type', 'timestamp']
    search_fields = ['original_text', 'conversation__user__username']
