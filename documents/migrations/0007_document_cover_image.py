# Generated by Django 2.2.2 on 2019-07-28 10:45

from django.db import migrations, models
import documents.models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_auto_20190723_0815'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='cover_image',
            field=models.ImageField(blank=True, max_length=1000, null=True, upload_to=documents.models.images, verbose_name='Image'),
        ),
    ]