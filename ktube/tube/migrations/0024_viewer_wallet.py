# Generated by Django 4.1.9 on 2023-06-07 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tube', '0023_video_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewer',
            name='wallet',
            field=models.BigIntegerField(default=0),
        ),
    ]