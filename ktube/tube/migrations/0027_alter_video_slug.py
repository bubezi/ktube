# Generated by Django 4.1.9 on 2023-06-07 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tube', '0026_alter_video_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='slug',
            field=models.SlugField(default='some_string', max_length=300, unique=True),
        ),
    ]
