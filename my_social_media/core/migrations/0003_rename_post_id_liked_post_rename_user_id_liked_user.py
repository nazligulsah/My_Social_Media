# Generated by Django 4.1.7 on 2023-03-20 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_user_id_post_user_alter_post_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='liked',
            old_name='post_id',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='liked',
            old_name='user_id',
            new_name='user',
        ),
    ]
