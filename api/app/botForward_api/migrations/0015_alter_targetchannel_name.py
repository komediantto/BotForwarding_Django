# Generated by Django 4.2 on 2023-05-10 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('botForward_api', '0014_alter_targetchannel_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='targetchannel',
            name='name',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Имя канала'),
        ),
    ]