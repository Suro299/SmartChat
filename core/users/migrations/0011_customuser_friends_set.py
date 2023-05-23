# Generated by Django 4.1.6 on 2023-05-22 19:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_customuser_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='friends_set',
            field=models.ManyToManyField(blank=True, related_name='friends', to=settings.AUTH_USER_MODEL),
        ),
    ]