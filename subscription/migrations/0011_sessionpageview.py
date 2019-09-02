# Generated by Django 2.2.2 on 2019-09-02 05:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0009_auto_20190814_1154'),
        ('subscription', '0010_plan_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionPageView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(blank=True, max_length=100, null=True, verbose_name='Package Name')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_pageviews', to='documents.Document')),
            ],
        ),
    ]
