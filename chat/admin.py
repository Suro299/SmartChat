from django.contrib import admin
from .models import ChatMessage, Chat

admin.site.register(Chat)


@admin.register(ChatMessage)
class ChatMessageModelAdmin(admin.ModelAdmin):
    list_display = ["id", "sender_username", "message", "chat_ids", "date_created"]
    search_fields = ["id", "sender__username", "message", "chat_messages__id", "date_created"]
    
    def sender_username(self, obj):
        return obj.sender.username
    sender_username.short_description = "Sender Username"

    def chat_ids(self, obj):
        return ", ".join([str(chat.id) for chat in obj.chat_messages.all()])
    chat_ids.short_description = "Chat IDs"