from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db import models

from register.utils import period
from django_resized import ResizedImageField

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
    profile_picture = ResizedImageField(quality=50, force_format="WEBP", null=True, blank=True)
    about = models.CharField(max_length=300, null=True, blank=True)
    subscribers = models.ManyToManyField(Viewer, related_name="Subscribed_viewers", blank=True)
    website_official = models.URLField(max_length=150, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    @property
    def profilePictureURL(self):
        return self.profile_picture.url
    
    def public_video_count(self):
        return self.video_set.filter(private=False, unlisted=False).count()  # type: ignore
           
    
class Video(models.Model):
    title = models.CharField(max_length=150, blank=False, null=True)
    video = models.FileField(blank=False, null=True)
    thumbnail = ResizedImageField(quality=75, force_format="WEBP", null=True, blank=False) # ResizedImageField(size=[300, 300], quality=75, force_format="WEBP", upload_to="images/")
    description = models.TextField(max_length=10000, null=True, blank=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(Channel, null=True, on_delete=models.CASCADE)
    private = models.BooleanField(default=False)
    unlisted = models.BooleanField(default=False)
    likes = models.PositiveBigIntegerField(default=0)
    dislikes = models.PositiveBigIntegerField(default=0)
    views = models.PositiveBigIntegerField(default=0)
    path = models.URLField(max_length=150, null=True, blank=True, unique=True)
    
    def __str__(self):
        return self.title
    
    @property
    def videoURL(self):
        return self.video.url
    
    @property
    def thumbnailURL(self):
        return self.thumbnail.url
    
    def upload_period(self):
        return period(self.upload_time)       
                            
                            
class Comment(models.Model):
    comment_text = models.TextField(max_length=500, null=True)
    video = models.ForeignKey(Video, null=True, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, null=True, on_delete=models.DO_NOTHING)
    likes = models.PositiveBigIntegerField(default=0)
    dislikes = models.PositiveBigIntegerField(default=0)
    commmented_on = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.comment_text

    def upload_period(self):
        return period(self.commmented_on)
        

class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply = models.TextField(max_length=500, null=True)
    channel = models.ForeignKey(Channel, null=True, on_delete=models.DO_NOTHING)
    likes = models.PositiveBigIntegerField(default=0)
    dislikes = models.PositiveBigIntegerField(default=0)
    replied_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.reply
    
    def upload_period(self):
        return period(self.replied_on)

class Playlist(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False, default="Playlist")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video, related_name='playlists', blank=True)
    views = models.PositiveBigIntegerField(default=0)
    public = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def video_count(self):
        return self.videos.count()
    
    def public_video_count(self):
        return self.videos.filter(private = False).count()
        
    def upload_period(self):
        return period(self.created_on)
    
class Watchlater(models.Model):
    viewer = models.OneToOneField(Viewer, null=True, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video, related_name='watch_later', blank=True) # type: ignore
    public = False
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "My watchlater"  
    
    def video_count(self):
        return self.videos.count()
    
    def public_video_count(self):
        return self.videos.filter(private = False).count()
        
    def upload_period(self):
        return period(self.created_on) 
    
class LikedVideos(models.Model):
    viewer = models.OneToOneField(Viewer, null=True, blank=True, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video, related_name='liked_videos', blank=True)
    public = False
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "My Liked Videos"  
    
    def video_count(self):
        return self.videos.count()
    
    def public_video_count(self):
        return self.videos.filter(private = False).count()
        
    def upload_period(self):
        return period(self.created_on) 
  
    
class DisLikedVideos(models.Model):
    viewer = models.OneToOneField(Viewer, null=True, blank=True, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video, related_name='disliked_videos', blank=True)
    public = False
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "My DisLiked Videos"  
    
    def video_count(self):
        return self.videos.count()
    
    def public_video_count(self):
        return self.videos.filter(private = False).count()
        
    def upload_period(self):
        return period(self.created_on) 
    