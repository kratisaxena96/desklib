# Generated by Django 2.2.2 on 2020-03-16 07:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('homework_help', '0008_auto_20200311_0912'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
