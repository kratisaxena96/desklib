# Generated by Django 2.2.2 on 2019-11-20 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_auto_20191120_0620'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='name',
            field=models.CharField(default='kush', max_length=50),
            preserve_default=False,
        ),
    ]
