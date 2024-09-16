# Generated by Django 5.1.1 on 2024-09-16 12:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_subtitle_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtitle',
            name='end_time',
            field=models.FloatField(default=1726488599.716584),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subtitle',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
