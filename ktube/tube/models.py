from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


GENDERS = (
    ('select', 'SELECT'),
    ('male','MALE'),
    ('female', 'FEMALE'),
    ('OTHER', 'OTHER'),
    ('prefer not to say', 'PREFER NOT TO SAY'),
)

# Create your models here.
class Viewer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=True, blank=False)
    email = models.EmailField(max_length=100, null=True, blank=False, unique=True)
    phone = PhoneNumberField(null=True, blank=False)
    gender = models.CharField(null=True, max_length=100, choices=GENDERS)
    
    def __str__(self):
        return self.username
        

class Channel(models.Model):
    user = models.ForeignKey(Viewer, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True, unique=True)
    about = models.CharField(max_length=300, null=True)
    subscribers = models.ManyToOneRel(field_name='subscribers', to=Viewer, field=Viewer)
    # subscribers = models.ManyToManyField(Viewer, related_name='subscribers')
    
    def __str__(self):
        return self.name
           
    
class Video(models.Model):
    title = models.CharField(max_length=150, blank=False, null=True)
    video = models.FileField(blank=False, null=True)
    thumbnail = models.ImageField(null=True, blank=False)
    description = models.TextField(max_length=10000, null=True, blank=True, default="Video Description")
    # path = models.URLField(max_length=150, null=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(Channel, null=True, on_delete=models.CASCADE)
    likes = models.BigIntegerField(default=0)
    dislikes = models.BigIntegerField(default=0)
    views = models.BigIntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    @property
    def videoURL(self):
        url = self.video.url
        return url
    
    @property
    def thumbnailURL(self):
        return self.thumbnail.url

    
class Comment(models.Model):
    comment_text = models.TextField(max_length=500, null=True)
    channel = models.ForeignKey(Channel, on_delete=models.DO_NOTHING)
    likes = models.BigIntegerField(default=0)
    dislikes = models.BigIntegerField(default=0)
    
    def __str__(self):
        return self.comment_text


class CommentReply(models.Model):
    reply = models.TextField(max_length=500, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.DO_NOTHING)
    likes = models.BigIntegerField(default=0)
    dislikes = models.BigIntegerField(default=0)
    
    def __str__(self):
        return self.reply


class Playlist(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False, default="Playlist")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video, blank=True)
    views = models.BigIntegerField(default=0)
    
    def __str__(self):
        return self.name
