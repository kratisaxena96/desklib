# Generated by Django 2.2.2 on 2019-12-27 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0016_document_redirect_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'permissions': [('change_document_author', 'Staff Can Assign Document Author')]},
        ),
    ]