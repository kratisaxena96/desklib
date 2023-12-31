# Generated by Django 2.2.2 on 2020-05-19 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0022_auto_20200212_0722'),
        ('uploads', '0004_upload_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='is_verified',
            field=models.BooleanField(default=False, verbose_name='Is verified'),
        ),
        migrations.AddField(
            model_name='upload',
            name='required_document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='required_document', to='documents.Document'),
        ),
        migrations.AlterField(
            model_name='upload',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='Is published'),
        ),
    ]
