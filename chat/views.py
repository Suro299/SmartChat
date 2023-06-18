from django.shortcuts import render, redirect
from .models import Chat, ChatMessage
from django.db.models import Q
from users.models import CustomUser
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def upadte_total_uread_messages(request):
    user_chats = Chat.objects.filter(Q(member_1=request.user) | Q(member_2=request.user))
    
    total_unread_messages = 0
    for i in user_chats:
        i.unread_messages = i.messages.filter(viewed = False).exclude(sender = request.user).count()
        total_unread_messages += i.unread_messages
        i.save()
    
    return JsonResponse({"unreaded_messages_count": total_unread_messages})



def update_chats(request):
    user_chats = Chat.objects.filter(Q(member_1=request.user) | Q(member_2=request.user))
    
    for i in user_chats:
        i.unread_messages = i.messages.filter(viewed = False).exclude(sender = request.user).count()
        i.save()
        
    data = []

    for i in user_chats:
        data.append({
            "member_1": {
                "id": i.member_1.id,
                "username": i.member_1.username,
                "avatar": i.member_1.avatar.url,
                "activity_visibility": i.member_1.activity_visibility,
                "date_joined": i.member_1.date_joined,
            },
            
            "member_2": {
                "id": i.member_2.id,
                "username": i.member_2.username,
                "avatar": i.member_2.avatar.url,
                "activity_visibility": i.member_2.activity_visibility,
                "date_joined": i.member_1.date_joined,
            },
            
            "unread_messages": i.unread_messages
        })
        
        
    return JsonResponse({"data": data})
    
        


def add_message(request, id):
    if request.method == "POST":
        chat = Chat.objects.filter(Q(member_1=request.user.id, member_2=id) | Q(member_1=id, member_2=request.user.id)).first()
        
        new_message = request.POST.get("new_message")
        reply_message_id = request.POST.get("reply_message_id")
        forward_to_users_id = request.POST.get("forward_to_users_id")
        delete_message = request.POST.get("delete_message")
        
        
        
        if new_message:
            chat_send = Chat.objects.get(id = chat.id)
            
            if reply_message_id:
                reply_message = ChatMessage.objects.get(id = reply_message_id)
                chat_send.messages.create(sender = request.user, message = new_message, reply_to = reply_message, forwarding_to = None)
            else:
                chat_send.messages.create(sender = request.user, message = new_message, reply_to = None, forwarding_to = None)
            chat_send.save()
        
        elif delete_message:
            message = chat.messages.get(id = delete_message)
            if message.sender == request.user:
                message.delete()    
        elif forward_to_users_id:
            message_id = request.POST.get("forwarding_id") 
            
            forwarding_chat = Chat.objects.filter(Q(member_1=request.user.id, member_2=forward_to_users_id) | Q(member_1=forward_to_users_id, member_2=request.user.id)).first()
            forwarding_message = ChatMessage.objects.get(id = int(message_id))
            
            forwarding_chat.messages.create(sender = request.user, message = forwarding_message.message, reply_to = None, forwarding_to = forwarding_message.sender)
            
        return JsonResponse({"success": True})
        
    return JsonResponse({"success": False})

def update_messages(request, id):
    chat = Chat.objects.filter(Q(member_1=request.user.id, member_2=id) | Q(member_1=id, member_2=request.user.id)).first()
    messages = chat.messages.all()
    data = []
    
    messages_to_update = chat.messages.filter(viewed=False).exclude(sender = request.user)

    if messages_to_update:
        for i in messages_to_update:
            i.viewed = True
            i.save()
    
    
    for i in messages:
        reply_to = None
        forwarding_to = None
        if i.reply_to:
            reply_to = {
                "username": i.reply_to.sender.username,
                "message": i.reply_to.message
            } 
            
        if i.forwarding_to:
            forwarding_to = {
                "id": i.forwarding_to.id,
                "username": i.forwarding_to.username,
            } 
            
        data.append({
            "id": i.id,
            "message": i.message,
            "date_created": i.date_created.strftime("%H:%M"),
            "reply_to": reply_to,
            "forwarding_to": forwarding_to,
            'viewed': i.viewed,
            "sender": {
                "id": i.sender.id,
                "username": i.sender.username
            }
        })
        
    return JsonResponse({"data": data})


def empty_chat(request):
    if not (request.user.is_authenticated):
        return redirect("login")
    
    user_chats = Chat.objects.filter(Q(member_1=request.user) | Q(member_2=request.user))
    
    total_unread_messages = 0
    for i in user_chats:
        i.unread_messages = i.messages.filter(viewed = False).exclude(sender = request.user).count()
        total_unread_messages += i.unread_messages
        i.save()
        
    print(total_unread_messages)
        
    return render(request, "chat/chat_list.html", {
        "user_chats": user_chats,
        "total_unread_messages": total_unread_messages,
        "page": "chats"
    })

def chat(request, id=None ):
    if not (request.user.is_authenticated):
        return redirect("login")
    
    user_chats = Chat.objects.filter(Q(member_1=request.user) | Q(member_2=request.user))
    
    total_unread_messages = 0
    for i in user_chats:
        i.unread_messages = i.messages.filter(viewed = False).exclude(sender = request.user).count()
        total_unread_messages += i.unread_messages
        i.save()
    
    chat = Chat.objects.filter(Q(member_1=request.user.id, member_2=id) | Q(member_1=id, member_2=request.user.id)).first()
    
    if chat:
        messages_to_update = chat.messages.filter(viewed=False)

        if messages_to_update:
            for i in messages_to_update:
                if i.sender != request.user:
                    i.viewed = True
                    i.save()
                
    else:
        new_chat = Chat.objects.create(member_1 = request.user, member_2 = CustomUser.objects.get(id = id) )
        chat = new_chat.id
            
    companion = CustomUser.objects.get(id = id)
    
    
    return render(request, "chat/chat.html", {
        "chat": chat,
        "user_chats": user_chats,
        "companion": companion,
        "total_unread_messages": total_unread_messages,
        "page": "chats"        
    })






