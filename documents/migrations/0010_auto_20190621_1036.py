# Generated by Django 2.2.2 on 2019-06-21 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0009_auto_20190621_1012'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='subject',
            new_name='subjects',
        ),
    ]
