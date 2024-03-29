# Generated by Django 4.2 on 2023-05-07 08:54

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('tube', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='profile_picture',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, null=True, quality=75, scale=None, size=[1920, 1080], upload_to=''),
        ),
    ]
