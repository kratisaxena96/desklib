# Generated by Django 2.2.2 on 2020-05-20 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0006_auto_20200520_0658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='upload',
            name='required_document',
        ),
    ]
