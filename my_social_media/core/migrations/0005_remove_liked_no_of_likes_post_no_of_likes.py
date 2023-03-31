# Generated by Django 4.1.7 on 2023-03-20 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_liked_post_liked_no_of_likes_liked_post_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='liked',
            name='no_of_likes',
        ),
        migrations.AddField(
            model_name='post',
            name='no_of_likes',
            field=models.IntegerField(default=0),
        ),
    ]