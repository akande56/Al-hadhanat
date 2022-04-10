# Generated by Django 3.1.11 on 2021-10-26 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Students', '0008_remove_subject_average'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='Exam',
            field=models.PositiveIntegerField(blank=True, default='0'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='assignment1',
            field=models.PositiveIntegerField(blank=True, default='0'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='assignment2',
            field=models.PositiveIntegerField(blank=True, default='0'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='test1',
            field=models.PositiveIntegerField(blank=True, default='0'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='test2',
            field=models.PositiveIntegerField(blank=True, default='0'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='total',
            field=models.PositiveIntegerField(blank=True, default='0'),
        ),
    ]
