# Generated by Django 4.1.9 on 2023-05-14 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tube', '0004_likedvideos'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisLikedVideos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('videos', models.ManyToManyField(blank=True, related_name='disliked_videos', to='tube.video')),
                ('viewer', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tube.viewer')),
            ],
        ),
    ]
