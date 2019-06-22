# Generated by Django 2.2.2 on 2019-06-21 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0001_initial'),
        ('documents', '0008_auto_20190621_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='subject',
            field=models.ManyToManyField(blank=True, db_index=True, null=True, related_name='subject_documents', to='subjects.Subject'),
        ),
        migrations.AlterField(
            model_name='document',
            name='college',
            field=models.ForeignKey(blank=True, null=True, on_delete='SET_NULL', related_name='college_documents', to='documents.College'),
        ),
        migrations.AlterField(
            model_name='document',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete='SET_NULL', related_name='course_code_documents', to='documents.Course'),
        ),
        migrations.AlterField(
            model_name='document',
            name='type',
            field=models.IntegerField(choices=[(1, 'Notes'), (2, 'Study Material'), (3, 'Assignment Brief'), (4, 'Book'), (5, 'Journal'), (6, 'Solution'), (7, 'Presentation'), (8, 'Thesis'), (9, 'Research Paper')], db_index=True, default=6),
        ),
    ]
