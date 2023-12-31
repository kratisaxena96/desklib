# Generated by Django 2.2.2 on 2019-08-01 07:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import documents.utils


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0006_auto_20190716_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='key',
            field=models.CharField(db_index=True, default=documents.utils.key_generator, editable=False, max_length=10, unique=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='plan_days',
            field=models.IntegerField(default=0, verbose_name='Plan Days'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
