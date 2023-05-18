# Generated by Django 4.1.9 on 2023-05-08 05:04

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ("tube", "0002_alter_channel_profile_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="channel",
            name="profile_picture",
            field=django_resized.forms.ResizedImageField(
                blank=True,
                crop=None,
                force_format="WEBP",
                keep_meta=True,
                null=True,
                quality=50,
                scale=None,
                size=[1920, 1080],
                upload_to="",
            ),
        ),
    ]