# Generated by Django 2.2.2 on 2019-06-27 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_sessions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersession',
            name='session',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sessions.Session'),
        ),
    ]