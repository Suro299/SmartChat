# Generated by Django 4.2 on 2023-04-28 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_tags_remove_postsmodel_post_tags_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postsmodel',
            name='post_tags',
            field=models.ManyToManyField(blank=True, to='main.tags'),
        ),
    ]
