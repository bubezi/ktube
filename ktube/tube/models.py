from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

from register.myFunctions import period

GENDERS = (
    ('select', 'SELECT'),
    ('male','MALE'),
    ('female', 'FEMALE'),
    ('OTHER', 'OTHER'),
    ('prefer not to say', 'PREFER NOT TO SAY'),
)


# Create your models here.
class Viewer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=True, blank=False)
    email = models.EmailField(max_length=100, null=True, blank=False, unique=True)
    phone = PhoneNumberField(null=True, blank=False)
    gender = models.CharField(null=True, max_length=30, choices=GENDERS)
    joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
    
    def age (self):
        return period(self.joined)
        

class Channel(models.Model):
    user = models.ForeignKey(Viewer, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True, unique=True)
    profile_picture = models.ImageField(null=True, blank=True)
    about = models.CharField(max_length=300, null=True, blank=True)
    subscribers = models.ManyToManyField(Viewer, related_name="Subscribed_viewers", blank=True)
    website_official = models.URLField(max_length=150, null=True)
    
    def __str__(self):
        return self.name
    
    @property
    def profilePictureURL(self):
        return self.profile_picture.url
           
    
class Video(models.Model):
    title = models.CharField(max_length=150, blank=False, null=True)
    video = models.FileField(blank=False, null=True)
    thumbnail = models.ImageField(null=True, blank=False)
    description = models.TextField(max_length=10000, null=True, blank=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(Channel, null=True, on_delete=models.CASCADE)
    private = models.BooleanField(default=False)
    unlisted = models.BooleanField(default=False)
    likes = models.BigIntegerField(default=0)
    dislikes = models.BigIntegerField(default=0)
    views = models.BigIntegerField(default=0)
    path = models.URLField(max_length=150, null=True, blank=True, unique=True)
    
    def __str__(self):
        return self.title
    
    @property
    def videoURL(self):
        url = self.video.url
        return url
    
    @property
    def thumbnailURL(self):
        return self.thumbnail.url
    
    def upload_period(self):
        return period(self.upload_time)
       
                            
                            
class Comment(models.Model):
    comment_text = models.TextField(max_length=500, null=True)
    video = models.ForeignKey(Video, null=True, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, null=True, on_delete=models.DO_NOTHING)
    likes = models.BigIntegerField(default=0)
    dislikes = models.BigIntegerField(default=0)
    commmented_on = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.comment_text

    def upload_period(self):
        return period(self.commmented_on)
        

class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply = models.TextField(max_length=500, null=True)
    channel = models.ForeignKey(Channel, null=True, on_delete=models.DO_NOTHING)
    likes = models.BigIntegerField(default=0)
    dislikes = models.BigIntegerField(default=0)
    replied_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.reply
    
    def upload_period(self):
        return period(self.replied_on)

class Playlist(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False, default="Playlist")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video, related_name='playlists', blank=True)
    views = models.BigIntegerField(default=0)
    public = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def video_count(self):
        video_count = self.videos.count()
        return video_count
        
    def upload_period(self):
        return period(self.created_on)