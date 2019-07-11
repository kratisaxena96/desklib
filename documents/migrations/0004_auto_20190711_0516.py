# Generated by Django 2.2.2 on 2019-07-11 05:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_auto_20190627_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='author_document', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='document',
            name='college',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='college_documents', to='documents.College'),
        ),
        migrations.AlterField(
            model_name='document',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course_code_documents', to='documents.Course'),
        ),
        migrations.AlterField(
            model_name='document',
            name='filename',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='filename'),
        ),
        migrations.AlterField(
            model_name='file',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='file',
            name='document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='document_file', to='documents.Document'),
        ),
        migrations.AlterField(
            model_name='page',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='page',
            name='document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='documents.Document'),
        ),
        migrations.AlterField(
            model_name='page',
            name='html',
            field=models.TextField(verbose_name='Page html'),
        ),
    ]
