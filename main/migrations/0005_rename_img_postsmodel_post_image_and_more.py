# Generated by Django 4.2 on 2023-04-21 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_postsmodel_sender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postsmodel',
            old_name='img',
            new_name='post_image',
        ),
        migrations.RenameField(
            model_name='postsmodel',
            old_name='content',
            new_name='post_text',
        ),
        migrations.RenameField(
            model_name='postsmodel',
            old_name='title',
            new_name='post_title',
        ),
    ]
