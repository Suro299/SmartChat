# Generated by Django 4.2 on 2023-05-10 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postsmodel',
            name='datatime',
            field=models.DateField(auto_now_add=True, verbose_name='Data'),
            preserve_default =False,
        ),
    ]