# Generated by Django 4.1.6 on 2023-04-22 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_postsmodel_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postsmodel',
            name='comments',
            field=models.PositiveBigIntegerField(blank=True, default=0, verbose_name='Comments Count'),
        ),
    ]
