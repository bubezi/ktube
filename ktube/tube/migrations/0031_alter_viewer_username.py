# Generated by Django 4.1.9 on 2023-06-07 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tube', '0030_alter_viewer_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewer',
            name='username',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
