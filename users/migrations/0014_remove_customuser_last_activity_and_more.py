# Generated by Django 4.1.6 on 2023-05-25 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_customuser_last_activity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='last_activity',
        ),
        migrations.AddField(
            model_name='customuser',
            name='activity_visibility',
            field=models.CharField(choices=[('all', 'all'), ('friends', 'friends'), ('nobody', 'nobody')], default='all', max_length=7),
        ),
    ]
