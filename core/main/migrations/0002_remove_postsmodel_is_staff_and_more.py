# Generated by Django 4.2 on 2023-04-21 17:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postsmodel',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='postsmodel',
            name='post_text',
        ),
        migrations.RemoveField(
            model_name='postsmodel',
            name='post_title',
        ),
        migrations.RemoveField(
            model_name='postsmodel',
            name='username',
        ),
        migrations.AddField(
            model_name='postsmodel',
            name='content',
            field=models.TextField(default='', verbose_name='Post Content'),
        ),
        migrations.AddField(
            model_name='postsmodel',
            name='dislike',
            field=models.PositiveBigIntegerField(blank=True, default=0, verbose_name='Dislikes Count'),
        ),
        migrations.AddField(
            model_name='postsmodel',
            name='img',
            field=models.ImageField(upload_to='', verbose_name='Post Image'),
        ),
        migrations.AddField(
            model_name='postsmodel',
            name='like',
            field=models.PositiveBigIntegerField(blank=True, default=0, verbose_name='Likes Count'),
        ),
        migrations.AddField(
            model_name='postsmodel',
            name='sender',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postsmodel',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='postsmodel',
            name='title',
            field=models.CharField(default='', max_length=255, verbose_name='Post Title'),
        ),
    ]
