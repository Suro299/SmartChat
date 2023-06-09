# Generated by Django 4.1.6 on 2023-06-05 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_chat_unread_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='reply_to',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='repl', to='chat.chatmessage'),
            preserve_default=False,
        ),
    ]
