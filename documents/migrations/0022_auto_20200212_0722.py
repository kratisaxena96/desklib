# Generated by Django 2.2.2 on 2020-02-12 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0021_auto_20200123_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='seo_title',
            field=models.CharField(help_text='Tip: Start every main word in the title with a capital letter, Keep title brief and descriptive that is relevant to the content of your pages.', max_length=90),
        ),
    ]
