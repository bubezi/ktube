# Generated by Django 4.1.9 on 2023-06-07 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tube', '0028_alter_video_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewer',
            name='wallet',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]