# Generated by Django 2.2.2 on 2019-11-26 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0006_auto_20191114_0355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='short_description',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Short description'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='sub_heading',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Sub heading'),
        ),
    ]
