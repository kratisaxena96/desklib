# Generated by Django 2.2.2 on 2021-01-19 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0015_auto_20201016_0638'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='uploadfordocument',
            options={'permissions': [('create_or_reject_pay_per_subscription', 'Staff Can Make or Reject Pay Per Subscription')], 'verbose_name': 'upload for document', 'verbose_name_plural': 'uploads for document'},
        ),
    ]
