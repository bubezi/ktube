# Generated by Django 4.1.9 on 2023-06-07 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tube', '0029_alter_viewer_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewer',
            name='wallet',
            field=models.FloatField(default=0),
        ),
    ]
