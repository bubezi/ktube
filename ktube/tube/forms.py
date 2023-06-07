from django import forms
from .models import Video, Playlist

class VideoForm(forms.ModelForm):
    
    class Meta:
        model = Video
        fields = ("title", "video", "thumbnail", "description", "private", "unlisted", "price")
        
    def save(self, channel, commit=True):
        video = super().save(commit=False)
        
        video.title = self.cleaned_data['title']
        video.video = self.cleaned_data['video']
        video.thumbnail = self.cleaned_data['thumbnail']
        video.description = self.cleaned_data['description']
        video.private = self.cleaned_data['private']
        video.unlisted = self.cleaned_data['unlisted']
        video.price = self.cleaned_data['price']
        video.channel = channel
        
        if commit:
            video.save()
            

class PlaylistForm(forms.ModelForm):
    
    class Meta:
        model = Playlist
        fields = ("name", "public",)
        
    def save(self, channel, commit=True):
        playlist = super().save(commit=False)
        
        playlist.name = self.cleaned_data['name']
        playlist.public = self.cleaned_data['public']
        playlist.channel = channel
        
        if commit:
            playlist.save()
            