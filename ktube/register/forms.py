from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from tube.models import GENDERS, Viewer, Channel, Watchlater, LikedVideos, DisLikedVideos, SavedPlaylists, Subscriptions



class ViewerForm(forms.ModelForm):
    # email = forms.EmailField(widget=forms.EmailInput())
    phone = PhoneNumberField(widget=forms.TextInput())
    gender = forms.ChoiceField(choices=GENDERS, widget=forms.Select())

    class Meta:
        model = Viewer
        fields = ["phone", "gender"]
        

class WatchlaterForm(forms.ModelForm):
    
    class Meta:
        model = Watchlater
        fields = ("viewer",)


class UserSignUpForm(UserCreationForm, WatchlaterForm, ViewerForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required', widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already taken')
        return email

    # def clean_phone(self):
    #     phone = self.cleaned_data['phone']
    #     if Viewer.objects.filter(phone=phone).exists():
    #         raise forms.ValidationError('Phone number is already taken')
    #     return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        

        try:
            viewer = user.viewer
        except Viewer.DoesNotExist:
            viewer = Viewer(user=user)
            
        try:
            watchlater = Watchlater.objects.get(viewer=viewer)
        except Watchlater.DoesNotExist:
            watchlater = Watchlater(viewer=viewer)
            
        try:
            savedPlaylists = SavedPlaylists.objects.get(viewer=viewer)
        except SavedPlaylists.DoesNotExist:
            savedPlaylists = SavedPlaylists(viewer=viewer)

        try:
            liked_videos = LikedVideos.objects.get(viewer=viewer)
        except LikedVideos.DoesNotExist:
            liked_videos = LikedVideos(viewer=viewer)
            
        try:
            disliked_videos = DisLikedVideos.objects.get(viewer=viewer)
        except DisLikedVideos.DoesNotExist:
            disliked_videos = DisLikedVideos(viewer=viewer)
            
        try:
            subscriptions = Subscriptions.objects.get(viewer=viewer)
        except Subscriptions.DoesNotExist:
            subscriptions = Subscriptions(viewer=viewer)
            
        viewer.username = self.cleaned_data['username']
        viewer.email = self.cleaned_data['email']
        viewer.phone = self.cleaned_data['phone']
        viewer.gender = self.cleaned_data['gender']
        
    
        
        if commit:
            viewer.save()
            watchlater.save()
            savedPlaylists.save()
            liked_videos.save()
            disliked_videos.save()
            subscriptions.save()

        return user


class ChangePhoneForm(forms.ModelForm):
    phone = PhoneNumberField(widget=forms.TextInput())

    class Meta:
        model = Viewer
        fields = ["phone"]
            
    def save(self, commit=True):
        viewer = super().save(commit=False)
        viewer.phone = self.cleaned_data['phone']
        if commit:
            viewer.save()
        return viewer
    
    
class ChangeGenderForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDERS, widget=forms.Select())

    class Meta:
        model = Viewer
        fields = ["gender"]
        

    def save(self, commit=True):
        viewer = super().save(commit=False)
        viewer.gender = self.cleaned_data['gender']
        if commit and not viewer.gender=='select':
            viewer.save()
        return viewer
    
class ChannelForm(forms.ModelForm):
            
    class Meta:
        model = Channel
        fields = ["name", "profile_picture", "about"]
        
    def save(self, viewer, commit=True):
        channel = super().save(commit=False)
        channel.user = viewer
        channel.name = self.cleaned_data['name']
        channel.profile_picture = self.cleaned_data['profile_picture']
        channel.about = self.cleaned_data['about']
        if commit:
            channel.save()
        return channel

    
class ChangeChannelNameForm(forms.ModelForm):
            
    class Meta:
        model = Channel
        fields = ["name"]
        
    def save(self, pk, commit=True):
        channel = Channel.objects.get(id=pk)
        channel.name = self.cleaned_data['name']
        if commit:
            channel.save()
        return channel

    
class ChangeChannelDPForm(forms.ModelForm):
            
    class Meta:
        model = Channel
        fields = ["profile_picture"]
        
    def save(self, pk, commit=True):
        channel = Channel.objects.get(id=pk) # type: ignore
        channel.profile_picture = self.cleaned_data['profile_picture']
        if commit:
            channel.save()
        return channel
        
        
class ChangeChannelAboutForm(forms.ModelForm):
            
    class Meta:
        model = Channel
        fields = ["about"]
        
    def save(self, pk, commit=True):
        channel = Channel.objects.get(id=pk)
        channel.about = self.cleaned_data['about']
        if commit:
            channel.save()
        return channel
        
        
class ChangeChannelWebsiteForm(forms.ModelForm):
            
    class Meta:
        model = Channel
        fields = ["website_official"]
        
    def save(self, pk, commit=True):
        channel = Channel.objects.get(id=pk)
        channel.website_official = self.cleaned_data['website_official']
        if commit:
            channel.save()
        return channel
