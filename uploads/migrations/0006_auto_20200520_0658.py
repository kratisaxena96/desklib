# Generated by Django 2.2.2 on 2020-05-20 06:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0022_auto_20200212_0722'),
        ('uploads', '0005_auto_20200519_0658'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadForDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_verified', models.BooleanField(default=False, verbose_name='Is verified')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='author_upload_document', to=settings.AUTH_USER_MODEL)),
                ('required_document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='upload_for_required_document', to='documents.Document')),
            ],
        ),
        migrations.AddField(
            model_name='upload',
            name='upload_for_document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='upload_for_document', to='uploads.UploadForDocument'),
        ),
    ]