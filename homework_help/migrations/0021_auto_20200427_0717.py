# Generated by Django 2.2.2 on 2020-04-27 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homework_help', '0020_auto_20200427_0635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='seo_description',
            field=models.TextField(blank=True, help_text='Tip: Create concise and high-quality descriptions that accurately describe your page, Make sure each page on our website has a different description.', max_length=160, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='seo_title',
            field=models.CharField(blank=True, help_text='Tip: Start every main word in the title with a capital letter, Keep title brief and descriptive that is relevant to the content of your pages.', max_length=90, null=True),
        ),
    ]
