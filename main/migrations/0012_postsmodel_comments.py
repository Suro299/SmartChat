# Generated by Django 4.2 on 2023-04-21 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_postsmodel_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='postsmodel',
            name='comments',
            field=models.PositiveBigIntegerField(blank=True, default=0, verbose_name='Dislikes Count'),
        ),
    ]
