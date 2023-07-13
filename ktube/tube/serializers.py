from rest_framework import serializers

from .models import *

class ViewerSerializer(serializers.ModelSerializer):
    class Meta:
        # db_table = ''
        # managed = True
        # verbose_name = 'Viewer'
        # verbose_name_plural = 'Viewers'
        model = Viewer
        fields = ('id', 'username', 'email', 'phone', 'gender', 'joined', 'wallet')
      
        
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'user', 'name', 'profile_picture', 'about', 'subscribers', 'website_official', 'channel_active')
        

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'title', 'video', 'thumbnail', 'description', 'upload_time', 'channel', 'private', 'unlisted', 'private', 'likes', 'dislikes', 'views', 'slug', 'path', 'price', 'paid_viewers')
        
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'comment_text', 'video', 'channel', 'likes', 'dislikes', 'commented_on')


class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReply
        fields = ('id', 'comment', 'reply', 'channel', 'likes', 'dislikes', 'replied_on')
        

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('id', 'name', 'channel', 'videos', 'views', 'public', 'created_on')
        

class WatchlaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlater
        fields = ('id', 'viewer', 'videos', 'public')

class LikedVideosSerializer(serializers.ModelSerializer):
    class Meta:
        models = LikedVideos
        fields = ('id', 'viewer', 'videos', 'public')
        

class DisLikedVideosSerializer(serializers.ModelSerializer):
    class Meta:
        models = DisLikedVideos
        fields = ('id', 'viewer', 'videos', 'public')
        

class SavedPlaylistsSerializer(serializers.ModelSerializer):
    class Meta:
        models = SavedPlaylists
        fields = ('id', 'viewer', 'playlists', 'public')
    

class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        models = Subscriptions
        fields = ('id', 'viewer', 'subscriptions', 'public')
        

class VideoViewSerializer(serializers.ModelSerializer):
    class Meta:
        models = VideoView
        fields = ('id', 'video', 'viewer', 'viewer_ip', 'viewed_on')
        
        
class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        models = History
        fields = ('id', 'viewer', 'views', 'public')
        
        
class LikedCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        models = LikedComments
        fields = ('id', 'viewer', 'comments')
    
class DisLikedCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        models = DisLikedComments
        fields = ('id', 'viewer', 'comments') 
    
class LikedCommentsRepliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedCommentsReplies
        fields = ('id', 'viewer', 'comment_replies')
    
    
class DisLikedCommentsRepliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisLikedCommentsReplies
        fields = ('id', 'viewer', 'comment_replies')
