# Generated by Django 3.1.2 on 2020-11-06 18:03

import cloudstore.apps.api.models.folder
from django.db import migrations, models

#
# Manually edited
# See https://stackoverflow.com/questions/29373887/django-db-utils-integrityerror-unique-constraint-failed-rango-category-new-sl
#


def gen_uuid(apps, schema_editor):
    Folder = apps.get_model('api', 'Folder')
    for row in Folder.objects.all():
        row.uuid = cloudstore.apps.api.models.folder.get_uuid()
        row.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20201019_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='uuid',
            field=models.CharField(
                default=cloudstore.apps.api.models.folder.get_uuid, max_length=8
            ),
        ),
        migrations.RunPython(gen_uuid),
        migrations.AlterField(
            model_name='folder',
            name='uuid',
            field=models.CharField(
                default=cloudstore.apps.api.models.folder.get_uuid, max_length=8, unique=True
            ),
        ),
    ]