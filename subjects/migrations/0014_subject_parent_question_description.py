# Generated by Django 2.2.2 on 2020-09-07 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0013_auto_20200622_0713'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='parent_question_description',
            field=models.TextField(blank=True, null=True, verbose_name='Parent Question description'),
        ),
    ]
