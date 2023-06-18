from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.empty_chat, name = "empty_chat"),
    path("<int:id>/", views.chat, name = "chat"),
    path("update_messages/<int:id>", views.update_messages, name = "update_messages"),
    path("add_message/<int:id>", views.add_message, name = "add_message"),
    path("update_chats/", views.update_chats, name = "update_chats"),
    path("upadte_total_uread_messages/", views.upadte_total_uread_messages, name = "upadte_total_uread_messages")
]