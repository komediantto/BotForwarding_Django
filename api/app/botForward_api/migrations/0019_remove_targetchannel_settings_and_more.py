# Generated by Django 4.2 on 2023-05-11 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botForward_api', '0018_remove_channel_settings_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='targetchannel',
            name='settings',
        ),
        migrations.AddField(
            model_name='targetchannel',
            name='forwarding',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Settings',
        ),
    ]
