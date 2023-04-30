from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from tube.models import Viewer

GENDERS = (
    ('select', 'SELECT'),
    ('male','MALE'),
    ('female', 'FEMALE'),
    ('OTHER', 'OTHER'),
    ('prefer not to say', 'PREFER NOT TO SAY'),
)


class ViewerForm(forms.ModelForm):
    # email = forms.EmailField(widget=forms.EmailInput())
    phone = PhoneNumberField(widget=forms.TextInput())
    gender = forms.ChoiceField(choices=GENDERS, widget=forms.Select())

    class Meta:
        model = Viewer
        fields = ["phone", "gender"]


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
        if commit:
            user.save()

        # Check if a viewer object already exists for the user
        try:
            viewer = user.viewer
        except Viewer.DoesNotExist:
            viewer = Viewer(user=user)

        viewer.phone = self.cleaned_data['phone']
        viewer.gender = self.cleaned_data['gender']
        
        if commit:
            viewer.save()

        return user


class ChangeUserDetailsForm(forms.ModelForm):
    phone = PhoneNumberField(widget=forms.TextInput())
    gender = forms.ChoiceField(choices=GENDERS, widget=forms.Select())

    class Meta:
        model = Viewer
        fields = ["phone", "gender"]

    def save(self, commit=True):
        viewer = super().save(commit=False)
        viewer.phone = self.cleaned_data['phone']
        viewer.gender = self.cleaned_data['gender']
        if commit:
            viewer.save()
        return viewer
