# Generated by Django 2.2.2 on 2019-06-21 09:40

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import documents.models
import documents.utils
import meta.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'colleges',
                'verbose_name': 'college',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('semester', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('college', models.ForeignKey(on_delete='PROTECT', related_name='college_course', to='documents.College')),
            ],
            options={
                'verbose_name_plural': 'courses',
                'verbose_name': 'course',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, default=documents.utils.key_generator, editable=False, max_length=10, unique=True)),
                ('title', models.CharField(db_index=True, max_length=200, verbose_name='Title')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('type', models.IntegerField(choices=[(1, 'Notes'), (2, 'Study Material'), (3, 'Assignment Brief'), (4, 'Book'), (5, 'Journal'), (6, 'Solution'), (7, 'Presentation'), (8, 'Thesis'), (9, 'Research Paper')], default=6)),
                ('keywords', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Keywords')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Description')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Content')),
                ('summary', models.TextField(blank=True, null=True, verbose_name='Summary')),
                ('initial_text', models.TextField(blank=True, null=True, verbose_name='Initial Text')),
                ('first_sentence', models.CharField(blank=True, max_length=1000, null=True, verbose_name='First Sentence')),
                ('upload_file', models.FileField(max_length=1000, upload_to=documents.models.upload_to, verbose_name='Upload File')),
                ('main_file', models.FileField(blank=True, max_length=1000, null=True, upload_to=documents.models.main_files, verbose_name=' Main File')),
                ('pdf_converted_file', models.FileField(blank=True, max_length=1000, null=True, upload_to=documents.models.pdf_converted_files, verbose_name=' Pdf converted file')),
                ('words', models.IntegerField(blank=True, null=True, verbose_name='Total Words')),
                ('page', models.IntegerField(blank=True, null=True, verbose_name='Total pages')),
                ('filename', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('is_published', models.BooleanField(default=False, verbose_name='Is Published')),
                ('is_visible', models.BooleanField(default=False, verbose_name='Is Visible')),
                ('published_date', models.DateTimeField(blank=True, null=True, verbose_name='Published Date')),
                ('created', models.DateTimeField(editable=False)),
                ('updated', models.DateTimeField()),
                ('seo_title', models.CharField(help_text='Tip: Start every main word in the title with a capital letter, Keep title brief and descriptive that is relevant to the content of your pages.', max_length=70)),
                ('seo_description', models.TextField(help_text='Tip: Create concise and high-quality descriptions that accurately describe your page, Make sure each page on our website has a different description.', max_length=160)),
                ('seo_keywords', models.CharField(help_text='Recommended max.length of relevant seo keyword is 140 characters', max_length=140)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete='PROTECT', related_name='author_document', to=settings.AUTH_USER_MODEL)),
                ('college', models.ForeignKey(blank=True, null=True, on_delete='SET_NULL', related_name='college_document', to='documents.College')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete='SET_NULL', related_name='course_code_document', to='documents.Course')),
            ],
            options={
                'verbose_name_plural': 'documents',
                'verbose_name': 'document',
            },
            bases=(meta.models.ModelMeta, models.Model),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'subjects',
                'verbose_name': 'subject',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(max_length=1000, upload_to=documents.models.images, verbose_name='Image')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete='SET_NULL', to=settings.AUTH_USER_MODEL)),
                ('document', models.ForeignKey(blank=True, null=True, on_delete='SET_NULL', related_name='document_image', to='documents.Document')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default=documents.utils.key_generator, editable=False, max_length=10, unique=True)),
                ('file', models.FileField(max_length=1000, upload_to=documents.models.all_files, verbose_name='File')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete='SET_NULL', to=settings.AUTH_USER_MODEL)),
                ('document', models.ForeignKey(blank=True, null=True, on_delete='SET_NULL', related_name='document_file', to='documents.Document')),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete='SET_NULL', related_name='subject_document', to='documents.Subject'),
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(on_delete='PROTECT', related_name='subject_course', to='documents.Subject'),
        ),
    ]
