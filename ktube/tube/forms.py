from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    
    class Meta:
        model = Video
        fields = ("title", "video", "thumbnail", "description", "private", "unlisted",)
        
    def save(self, channel, commit=True):
        video = super().save(commit=False)
        
        video.title = self.cleaned_data['title']
        video.video = self.cleaned_data['video']
        video.thumbnail = self.cleaned_data['thumbnail']
        video.description = self.cleaned_data['description']
        video.private = self.cleaned_data['private']
        video.unlisted = self.cleaned_data['unlisted']
        video.channel = channel
        
        if commit:
            video.save()
        
            
