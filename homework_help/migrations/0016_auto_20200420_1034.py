# Generated by Django 2.2.2 on 2020-04-20 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homework_help', '0015_answerfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answerfile',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answerfiles', to='homework_help.Answers'),
        ),
    ]
