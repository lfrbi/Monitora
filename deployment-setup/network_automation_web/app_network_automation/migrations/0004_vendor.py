# Generated by Django 3.2.25 on 2024-12-18 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_network_automation', '0003_alter_log_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]
