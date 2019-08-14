# Generated by Django 2.2.2 on 2019-08-12 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0002_subject_parent_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='parent_subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subjects.Subject', verbose_name='Parent Subject'),
        ),
    ]