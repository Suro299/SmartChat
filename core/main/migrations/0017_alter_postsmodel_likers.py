# Generated by Django 4.1.6 on 2023-04-22 19:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0016_postsmodel_likers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postsmodel',
            name='likers',
            field=models.ManyToManyField(blank=True, related_name='likers', to=settings.AUTH_USER_MODEL),
        ),
    ]