# Generated by Django 3.2.3 on 2021-06-04 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='invites',
        ),
    ]
