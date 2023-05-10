# Generated by Django 4.2 on 2023-05-10 13:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0027_delete_postsmodel_delete_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Tag Name')),
            ],
        ),
        migrations.CreateModel(
            name='PostsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(max_length=255, verbose_name='Post Title')),
                ('post_text', models.TextField(verbose_name='Post Content')),
                ('post_image', models.ImageField(blank=True, upload_to='', verbose_name='Post Image')),
                ('comments', models.PositiveBigIntegerField(blank=True, default=0, verbose_name='Comments Count')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('dislikers', models.ManyToManyField(blank=True, related_name='dislikers', to=settings.AUTH_USER_MODEL)),
                ('likers', models.ManyToManyField(blank=True, related_name='likers', to=settings.AUTH_USER_MODEL)),
                ('post_tags', models.ManyToManyField(blank=True, to='main.tag')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]