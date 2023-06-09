# Generated by Django 4.1.6 on 2023-05-27 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Films',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Title')),
                ('img', models.URLField(max_length=255, verbose_name='Url')),
                ('year', models.PositiveIntegerField(verbose_name='Year')),
                ('genre', models.CharField(max_length=255, verbose_name='Genre')),
            ],
        ),
    ]
