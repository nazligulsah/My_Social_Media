# Generated by Django 4.1.7 on 2023-03-20 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_rename_followed_user_id_follow_followed_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='followed_user',
            field=models.CharField(max_length=250),
        ),
    ]
