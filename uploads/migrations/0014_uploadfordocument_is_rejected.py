# Generated by Django 2.2.2 on 2020-08-31 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0013_auto_20200529_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfordocument',
            name='is_rejected',
            field=models.BooleanField(default=False, verbose_name='Is rejected'),
        ),
    ]