# Generated by Django 4.2 on 2023-04-28 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_alter_postsmodel_post_tags'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tags',
            new_name='Tag',
        ),
    ]
