# Generated by Django 2.2.2 on 2020-04-28 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_auto_20200413_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogmodel',
            name='cover_image',
            field=models.ImageField(upload_to='photos'),
        ),
        migrations.AlterField(
            model_name='blogmodel',
            name='published_date',
            field=models.DateTimeField(),
        ),
    ]
