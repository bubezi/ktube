# Generated by Django 4.2 on 2023-05-05 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tube', '0005_alter_channel_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='private',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='video',
            name='unlisted',
            field=models.BooleanField(default=False),
        ),
    ]
