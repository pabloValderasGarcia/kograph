# Generated by Django 5.0.1 on 2024-02-11 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
