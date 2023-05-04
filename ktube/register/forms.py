from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from tube.models import GENDERS, Viewer, Channel



class ViewerForm(forms.ModelForm):
    # email = forms.EmailField(widget=forms.EmailInput())
    phone = PhoneNumberField(widget=forms.TextInput())
    gender = forms.ChoiceField(choices=GENDERS, widget=forms.Select())

    class Meta:
        model = Viewer
        fields = ["phone", "gender"]


class ChannelForm(forms.ModelForm):
            
    class Meta:
        model = Channel
        fields = ["name", "profile_picture", "about"]
        
    def save(self, pk, commit=True):
        
        user = Viewer.objects.get(id=pk)
        channel = super().save(commit=False)
        channel.user = user
        channel.name = self.cleaned_data['name']
        channel.profile_picture = self.cleaned_data['profile_picture']
        channel.about = self.cleaned_data['about']
        if commit:
            channel.save()
        return channel
    
class ChangeChannelForm(forms.ModelForm):
            
    class Meta:
        model = Channel
        fields = ["name", "profile_picture", "about"]
        
    def save(self, pk, commit=True):
        channel = Channel.objects.get(id=pk)
        channel.name = self.cleaned_data['name']
        channel.profile_picture = self.cleaned_data['profile_picture']
        channel.about = self.cleaned_data['about']
        print(channel.profile_picture, "!!!!!!!!!!!!                         !!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(channel.about, "!!!!!!!!!!!!                         !!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        if commit:
            channel.save()
        return channel
        


class UserSignUpForm(UserCreationForm, ViewerForm):
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

        # Check if a viewer object already exists for the user
        try:
            viewer = user.viewer
        except Viewer.DoesNotExist:
            viewer = Viewer(user=user)

        viewer.username = self.cleaned_data['username']
        viewer.email = self.cleaned_data['email']
        viewer.phone = self.cleaned_data['phone']
        viewer.gender = self.cleaned_data['gender']
    
        
        if commit:
            viewer.save()

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
    
