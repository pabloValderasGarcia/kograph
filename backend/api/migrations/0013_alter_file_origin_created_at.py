# Generated by Django 5.0 on 2024-01-08 22:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_file_origin_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='origin_created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
