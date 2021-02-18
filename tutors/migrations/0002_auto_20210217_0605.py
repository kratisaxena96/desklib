# Generated by Django 2.2.2 on 2021-02-17 06:05

from django.db import migrations, models
import tutors.models


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutor',
            name='profile_pic',
            field=models.ImageField(blank=True, max_length=500, upload_to=tutors.models.img_uploads, verbose_name='profile_pic'),
        ),
    ]
