# Generated by Django 4.2 on 2023-04-21 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_postsmodel_content_alter_postsmodel_img_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postsmodel',
            name='sender',
        ),
    ]
