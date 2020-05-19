# Generated by Django 2.2.2 on 2020-05-19 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homework_help', '0027_question_published_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Is Published'),
        ),
        migrations.AlterField(
            model_name='question',
            name='is_visible',
            field=models.BooleanField(default=False, verbose_name='Is Visible'),
        ),
    ]
