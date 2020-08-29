# Generated by Django 3.1 on 2020-08-26 14:29

import cloudstore.apps.api.models.file
from django.db import migrations
import private_storage.fields
import private_storage.storage.files


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200823_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='thumb',
            field=cloudstore.apps.api.models.file.NotRequiredPrivateFileField(
                blank=True, null=True, storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to=cloudstore.apps.api.models.file.get_thumbnail_filename),
        ),
    ]
