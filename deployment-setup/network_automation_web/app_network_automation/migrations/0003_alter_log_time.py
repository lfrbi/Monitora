# Generated by Django 3.2.25 on 2024-12-06 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_network_automation', '0002_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='time',
            field=models.DateTimeField(null=True),
        ),
    ]
