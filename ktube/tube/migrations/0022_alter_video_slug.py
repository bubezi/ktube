# Generated by Django 4.1.9 on 2023-06-07 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tube', '0021_video_slug_alter_video_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='slug',
            field=models.SlugField(default='some-string', max_length=300, unique=True),
        ),
    ]
