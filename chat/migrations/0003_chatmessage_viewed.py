# Generated by Django 4.1.6 on 2023-06-03 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatmessage_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='viewed',
            field=models.BooleanField(default=False, verbose_name='Viewed'),
        ),
    ]
