# Generated by Django 4.1.9 on 2023-05-15 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tube', '0012_remove_history_view_history_views'),
    ]

    operations = [
        migrations.RenameField(
            model_name='history',
            old_name='views',
            new_name='view',
        ),
    ]
