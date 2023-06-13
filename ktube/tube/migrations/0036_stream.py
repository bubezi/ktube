# Generated by Django 4.1.9 on 2023-06-12 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tube', '0035_videoview_viewer_ip'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=32, unique=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(default='LIVE Stream', max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='')),
                ('visibility', models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default='public', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tube.viewer')),
            ],
        ),
    ]
