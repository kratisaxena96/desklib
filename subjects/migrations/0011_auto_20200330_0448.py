# Generated by Django 2.2.2 on 2020-03-30 04:48

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0010_auto_20200323_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjectcontent',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Description'),
        ),
    ]