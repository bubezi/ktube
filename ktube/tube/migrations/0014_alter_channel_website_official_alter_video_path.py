# Generated by Django 4.2 on 2023-05-06 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tube', '0013_alter_video_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='website_official',
            field=models.URLField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='path',
            field=models.URLField(blank=True, max_length=150, null=True, unique=True),
        ),
    ]
