# Generated by Django 3.2.25 on 2024-12-22 06:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_network_automation', '0008_auto_20241220_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
