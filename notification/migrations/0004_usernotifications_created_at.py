# Generated by Django 3.2.3 on 2021-07-13 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_expotoken_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernotifications',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
