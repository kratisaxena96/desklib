# Generated by Django 2.2.2 on 2020-04-27 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homework_help', '0021_auto_20200427_0717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Is Paid'),
        ),
    ]
