# Generated by Django 3.2.3 on 2021-07-09 15:25

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20210709_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='created_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='posts',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=15), blank=True, null=True, size=None),
        ),
    ]