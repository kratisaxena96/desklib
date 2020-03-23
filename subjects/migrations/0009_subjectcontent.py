# Generated by Django 2.2.2 on 2020-03-20 06:44

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0008_auto_20191126_0621'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Description')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_code_documents', to='subjects.Subject')),
            ],
            options={
                'verbose_name': 'subject content',
                'verbose_name_plural': 'subject content',
            },
        ),
    ]
