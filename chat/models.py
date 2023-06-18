from django.db import models
from users.models import CustomUser
from django.utils import timezone

class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete = models.DO_NOTHING)
    message = models.TextField("Message")
    viewed = models.BooleanField("Viewed", default = False)
    date_created = models.DateTimeField("Data Created", auto_created = True, default = timezone.now)
    reply_to = models.ForeignKey("ChatMessage", related_name = "repl", on_delete = models.CASCADE, blank = True, null = True)
    forwarding_to = models.ForeignKey(CustomUser, related_name = "forwarding", on_delete = models.DO_NOTHING, blank = True, null = True)
    
    def __str__(self) -> str:
        return f"{self.id} {self.sender.username}"


class Chat(models.Model):
    member_1 = models.ForeignKey(CustomUser, related_name = "member1", on_delete = models.DO_NOTHING)
    member_2 = models.ForeignKey(CustomUser, related_name = "member2", on_delete = models.DO_NOTHING)
    messages = models.ManyToManyField(ChatMessage, related_name = "chat_messages", blank = True)  
    unread_messages = models.PositiveIntegerField("Unread Messages", default = 0)
    
    def __str__(self) -> str:
        return f"{self.id} | {self.member_1} <-> {self.member_2}"