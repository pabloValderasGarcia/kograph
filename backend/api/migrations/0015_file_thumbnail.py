# Generated by Django 5.0 on 2024-01-09 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_file_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails/'),
        ),
    ]