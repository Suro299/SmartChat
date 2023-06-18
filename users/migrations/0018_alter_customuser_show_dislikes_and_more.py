# Generated by Django 4.1.6 on 2023-05-29 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_remove_customuser_hide_dislikes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='show_dislikes',
            field=models.BooleanField(default=False, verbose_name='Show Dislikes'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='show_favorites',
            field=models.BooleanField(default=False, verbose_name='Show Favorites'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='show_likes',
            field=models.BooleanField(default=False, verbose_name='Show Likes'),
        ),
    ]
