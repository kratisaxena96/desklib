# Generated by Django 2.2.2 on 2020-12-28 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0027_auto_20201217_0557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='total_downloads_to_show',
        ),
    ]
