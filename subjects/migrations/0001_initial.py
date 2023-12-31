# Generated by Django 2.2.2 on 2019-06-21 08:50

import ckeditor.fields
from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='Title')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Description')),
                ('is_visible', models.BooleanField(default=True, verbose_name='Is visible')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('keywords', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name_plural': 'subjects',
                'verbose_name': 'subject',
            },
        ),
    ]
