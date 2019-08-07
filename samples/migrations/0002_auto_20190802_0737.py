# Generated by Django 2.2.2 on 2019-08-02 07:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('samples', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='author_samples', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
