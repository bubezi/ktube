from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db import models
from django.utils.crypto import get_random_string
from ktube.settings import MEDIA_URL


from .utils import period
from django_resized import ResizedImageField


GENDERS = (
    ("select", "SELECT"),
    ("male", "MALE"),
    ("female", "FEMALE"),
    ("OTHER", "OTHER"),
    ("prefer not to say", "PREFER NOT TO SAY"),
)


# Create your models here.
class Viewer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)  # type: ignore
    username = models.CharField(max_length=100, null=True, blank=False, unique=True)
    email = models.EmailField(max_length=100, null=True, blank=False, unique=True)
    phone = PhoneNumberField(null=True, blank=False)
    gender = models.CharField(null=True, max_length=30, choices=GENDERS)
    joined = models.DateTimeField(auto_now_add=True)
    # wallet = models.PositiveBigIntegerField(default=0)
    wallet = models.FloatField(default=0)

    def __str__(self):
        return self.username

    def deposit(self, ammount):
        ammount = float(ammount)
        self.wallet += ammount

    def spend(self, ammount):
        ammount = float(ammount)
        if self.wallet >= ammount:
            self.wallet -= ammount
            return True
        else:
            return False

    def age(self):
        return period(self.joined)


class Channel(models.Model):
    user = models.ForeignKey(Viewer, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True, unique=True)
    profile_picture = ResizedImageField(
        quality=50, force_format="WEBP", null=True, blank=True
    )
    about = models.CharField(max_length=300, null=True, blank=True)
    subscribers = models.ManyToManyField(Viewer, related_name="Subscribed_viewers", blank=True)  # type: ignore
    website_official = models.URLField(max_length=150, null=True, blank=True)
    channel_active = models.BooleanField(default=True)

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
    thumbnail = ResizedImageField(
        quality=75, force_format="WEBP", null=True, blank=False
    )  # ResizedImageField(size=[300, 300], quality=75, force_format="WEBP", upload_to="images/")
    description = models.TextField(max_length=10000, null=True, blank=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(Channel, null=True, on_delete=models.CASCADE)
    private = models.BooleanField(default=False)
    unlisted = models.BooleanField(default=False)
    likes = models.PositiveBigIntegerField(default=0)
    dislikes = models.PositiveBigIntegerField(default=0)
    views = models.PositiveBigIntegerField(default=0)
    slug = models.SlugField(
        max_length=300, null=False, default="some_string", unique=True
    )
    path = models.URLField(max_length=450, null=True, blank=True, unique=True)
    # price = models.PositiveBigIntegerField(default=0)
    price = models.FloatField(default=0)
    paid_viewers = models.ManyToManyField(
        Viewer, related_name="paid_viewers", blank=True
    )

    def __str__(self):
        return self.title

    @property
    def videoURL(self):
        return self.video.url

    @property
    def videoFilename(self):
        start = len(MEDIA_URL)
        return str(self.videoURL)[start:]

    @property
    def thumbnailURL(self):
        return self.thumbnail.url

    @property
    def thumbnailFilename(self):
        start = len(MEDIA_URL)
        return str(self.thumbnailURL)[start:]

    def upload_period(self):
        return period(self.upload_time)

    def save(self, *args, **kwargs):
        # Generate the slug from the title before
        RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyz"
        RANDOM_STRING_CHARS += ""
        if self.slug == "some_string":
            self.slug = get_random_string(64, RANDOM_STRING_CHARS)
        super().save(*args, **kwargs)


class Comment(models.Model):
    comment_text = models.TextField(max_length=500, null=True)
    video = models.ForeignKey(Video, null=True, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, null=True, on_delete=models.CASCADE)
    likes = models.PositiveBigIntegerField(default=0)
    dislikes = models.PositiveBigIntegerField(default=0)
    commented_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text

    def upload_period(self):
        return period(self.commmented_on)


class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply = models.TextField(max_length=500, null=True)
    channel = models.ForeignKey(Channel, null=True, on_delete=models.CASCADE)
    likes = models.PositiveBigIntegerField(default=0)
    dislikes = models.PositiveBigIntegerField(default=0)
    replied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reply

    def upload_period(self):
        return period(self.replied_on)


class Playlist(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False, default="Playlist")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)  # type: ignore
    videos = models.ManyToManyField(Video, related_name="playlists", blank=True)  # type: ignore
    views = models.PositiveBigIntegerField(default=0)
    public = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def video_count(self):
        return self.videos.count()

    def public_video_count(self):
        return self.videos.filter(private=False).count()

    def upload_period(self):
        return period(self.created_on)


class Watchlater(models.Model):
    viewer = models.OneToOneField(Viewer, null=True, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video, related_name="watch_later", blank=True)  # type: ignore
    public = False

    def __str__(self):
        return self.viewer.username + " My watchlater"

    def video_count(self):
        return self.videos.count()

    def public_video_count(self):
        return self.videos.filter(private=False).count()


class LikedVideos(models.Model):
    viewer = models.OneToOneField(Viewer, null=True, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video, related_name="liked_videos", blank=True)
    public = False

    def __str__(self):
        return self.viewer.username + " My Liked Videos"

    def video_count(self):
        return self.videos.count()

    def public_video_count(self):
        return self.videos.filter(private=False).count()


class DisLikedVideos(models.Model):
    viewer = models.OneToOneField(Viewer, null=True, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video, related_name="disliked_videos", blank=True)
    public = False

    def __str__(self):
        return self.viewer.username + " My DisLiked Videos"

    def video_count(self):
        return self.videos.count()

    def public_video_count(self):
        return self.videos.filter(private=False).count()


class SavedPlaylists(models.Model):
    viewer = models.OneToOneField(Viewer, null=True, on_delete=models.CASCADE)
    playlists = models.ManyToManyField(
        Playlist, related_name="saved_playlists", blank=True
    )
    public = False

    def __str__(self):
        return self.viewer.username + " Saved Playlists"

    def playlist_count(self):
        return self.playlists.count()


class Subscriptions(models.Model):
    viewer = models.OneToOneField(Viewer, null=True, on_delete=models.CASCADE)
    subscriptions = models.ManyToManyField(
        Channel, related_name="subscriptions", blank=True
    )
    public = False

    def __str__(self):
        return self.viewer.username + " My Subscriptions"

    def playlist_count(self):
        return self.subscriptions.count()


class VideoView(models.Model):
    video = models.ForeignKey(Video, null=True, on_delete=models.CASCADE)
    viewer = models.ForeignKey(Viewer, null=True, on_delete=models.CASCADE)
    viewer_ip = models.GenericIPAddressField(
        null=True, protocol="both", unpack_ipv4=False
    )
    viewed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (
            "Title : "
            + str(self.video)
            + ", watched by: "
            + str(self.viewer)
            + ", watched: "
            + str(self.viewed_on)
            + ", IP address: "
            + str(self.viewer_ip)
        )


class History(models.Model):
    viewer = models.OneToOneField(Viewer, null=True, on_delete=models.CASCADE)
    views = models.ManyToManyField(VideoView, related_name="history", blank=True)
    public = False

    def __str__(self):
        return self.viewer.username + " My History"

    def video_count(self):
        return self.views.count()


class LikedComments(models.Model):
    viewer = models.OneToOneField(Viewer, null=True, on_delete=models.CASCADE)
    comments = models.ManyToManyField(
        Comment, related_name="liked_comments", blank=True
    )

    def __str__(self):
        return self.viewer.username + " Liked comments"


class DisLikedComments(models.Model):
    viewer = models.OneToOneField(Viewer, null=True, on_delete=models.CASCADE)
    comments = models.ManyToManyField(
        Comment, related_name="disliked_comments", blank=True
    )

    def __str__(self):
        return self.viewer.username + " Disliked comments"


class LikedCommentsReplies(models.Model):
    viewer = models.OneToOneField(Viewer, null=True, on_delete=models.CASCADE)
    comment_replies = models.ManyToManyField(
        CommentReply, related_name="liked_comment_replies", blank=True
    )

    def __str__(self):
        return self.viewer.username + " Liked comments replies"


class DisLikedCommentsReplies(models.Model):
    viewer = models.OneToOneField(Viewer, null=True, on_delete=models.CASCADE)
    comment_replies = models.ManyToManyField(
        CommentReply, related_name="disliked_comment_replies", blank=True
    )

    def __str__(self):
        return self.viewer.username + " Disliked comment replies"


class Stream(models.Model):
    viewer = models.ForeignKey(Viewer, on_delete=models.CASCADE)
    key = models.CharField(max_length=32, unique=True)
    started_at = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=255, null=False, default="LIVE Stream")
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(blank=True, null=True)
    PUBLIC = "public"
    PRIVATE = "private"
    VISIBILITY_CHOICES = [
        (PUBLIC, "Public"),
        (PRIVATE, "Private"),
    ]
    visibility = models.CharField(
        max_length=10, choices=VISIBILITY_CHOICES, default=PUBLIC
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.viewer.username + " My History"
