# Generated by Django 3.1.11 on 2021-11-23 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teachers', '0004_auto_20211121_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='middlename',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
