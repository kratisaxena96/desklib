# Generated by Django 2.2.2 on 2020-08-24 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_sessions', '0003_merge_20190703_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersession',
            name='user_agent',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]