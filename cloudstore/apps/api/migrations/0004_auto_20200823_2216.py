# Generated by Django 3.0.8 on 2020-08-23 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200802_1500'),
    ]

    operations = [
        migrations.RenameField(
            model_name='folder',
            old_name='parent',
            new_name='folder',
        ),
    ]
