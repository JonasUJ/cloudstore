# Generated by Django 3.1 on 2020-08-27 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloudstore', '0005_usersettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='view_img',
            field=models.BooleanField(default=True),
        ),
    ]