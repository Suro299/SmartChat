# Generated by Django 4.2 on 2023-05-10 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_remove_postsmodel_datatime_postsmodel_date_created'),
        ('users', '0005_alter_customuser_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='favorites',
            field=models.ManyToManyField(to='main.postsmodel'),
        ),
    ]
