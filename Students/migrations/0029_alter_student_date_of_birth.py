# Generated by Django 3.2.12 on 2024-02-11 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Students', '0028_auto_20240116_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='date_of_birth',
            field=models.DateField(help_text='year-month-date: e.g 2023-1-30'),
        ),
    ]
