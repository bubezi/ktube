from .forms import UserSignUpForm, ChangePhoneForm, ChangeGenderForm, ChangeChannelNameForm, ChangeChannelDPForm, ChangeChannelAboutForm, ChangeChannelWebsiteForm, ChannelForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from tube.models import Viewer, Channel, Watchlater
from .utils import check_errors
from django.http import HttpResponseForbidden, HttpResponseBadRequest


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token  # new

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate token or get the existing token.
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)  # updated
        else:
            return Response({"error": "Invalid username/password."}, status=status.HTTP_400_BAD_REQUEST)



# Create your views here.
def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = UserSignUpForm(request.POST, request.FILES) # type: ignore
            if form.is_valid():
                form.save()
                new_user = authenticate(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        )
                login(request, new_user)
                return redirect('/')
            else:
                errors = check_errors(form)
                form = UserSignUpForm()
                context = {"form": form, "errors": errors}

        else:
            form = UserSignUpForm()
            context = {"form": form}

        return render(request, "registration/register.html", context)
    else:
        return redirect('/')


def bye_page(request):
    context = {}
    return render(request, "registration/bye.html", context)


def profile_page(request):        
    if request.user.is_authenticated:
        viewer = request.user.viewer
        try:
            watchlater = Watchlater.objects.get(viewer=viewer)
        except Watchlater.DoesNotExist:
            watchlater = Watchlater(viewer=viewer)
            watchlater.save()
        context={'viewer': viewer, 'many_channels': False, "watchlater" : watchlater}
        try:
            channel = Channel.objects.get(user=viewer)
            context['channel']=channel
            context['nav_channel']=channel
            context['many_channels'] = False
            context['no_channel'] = False
        except Channel.DoesNotExist:
            context['many_channels'] = False
            context['no_channel'] = True
        except:
            context['many_channels'] = True
            context['no_channel'] = False
            
        if context['many_channels']:
            my_channels = Channel.objects.filter(user=viewer)
            context['my_channels'] = my_channels
            
            
        if request.method == "POST":
            form = ChangePhoneForm(request.POST, request.FILES, instance=viewer)
            form2 = ChangeGenderForm(request.POST, request.FILES, instance=viewer)
            if not request.POST.__contains__('phone'):
                if form2.is_valid:
                    form2.save()
                    return redirect('profile')
                else:
                    errors = check_errors(form2)
                    form = ChangePhoneForm()
                    form2 = ChangeGenderForm()
                    context['form']= form
                    context['form2']= form2
                    context['errors']= errors
            elif form.is_valid:
                form.save()
                return redirect('profile')
            else:
                errors = check_errors(form)
                errors2 = check_errors(form2)
                errors += errors2
                form = ChangePhoneForm()
                form2 = ChangeGenderForm()
                context['form']= form
                context['form2']= form2
                context['errors']= errors
        else:
            form = ChangePhoneForm()
            form2 = ChangeGenderForm()
            context['form']= form
            context['form2']= form2
        return render(request, "registration/profile.html", context)
    else:
        return redirect('login')
    
    
def create_channel(request):
    if request.user.is_authenticated:    
        viewer = request.user.viewer
        if request.method == "POST":
            form = ChannelForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    form.save(viewer)
                    return redirect('/')
                except Viewer.DoesNotExist as e:
                    form = ChannelForm()
                    context = {"form": form, "errors": e, "no_channel": True}
            else:
                errors = check_errors(form)
                form = ChannelForm()
                context = {"form": form, "errors": errors, "no_channel": True}

        else:
            form = ChannelForm()
            context = {"form": form, "no_channel": True}
        return render(request, 'registration/create_channel.html', context)
    else:
        return redirect('login')
    

def edit_channel(request, pk):
    if request.user.is_authenticated:
        viewer = request.user.viewer
        context={'viewer': viewer}
        try:
            channel = Channel.objects.get(id=pk) # type: ignore
            context['channel']=channel
            context['nav_channel']=channel
            context['no_channel'] = False
            context['many_channels'] = False
        except Channel.DoesNotExist as e:
            context['no_channel'] = True
            return HttpResponseBadRequest(e)
            
        owner = False
        if channel.user == viewer:
            owner = True          
            
        if owner:
            if request.method == "POST":
                form = ChangeChannelNameForm(request.POST, request.FILES)
                form2 = ChangeChannelDPForm(request.POST, request.FILES)
                form3 = ChangeChannelAboutForm(request.POST, request.FILES)
                form4 = ChangeChannelWebsiteForm(request.POST, request.FILES)
                if request.POST.__contains__('name'):
                    if form.is_valid():
                        form.save(pk)
                        return redirect(f'/edit_channel/{pk}')
                    else:
                        errors = check_errors(form)
                        form = ChangeChannelNameForm()
                        form2 = ChangeChannelDPForm()
                        form3 = ChangeChannelAboutForm()
                        form4 = ChangeChannelWebsiteForm()
                        context['form']= form
                        context['form2']= form2
                        context['form3']= form3
                        context['form4']= form4
                        context['no_channel']= False
                        context['errors']= errors
                        
                elif request.FILES.__contains__('profile_picture'):
                    if form2.is_valid():
                        form2.save(pk)
                        return redirect(f'/edit_channel/{pk}')
                    else:
                        errors = check_errors(form2)
                        form = ChangeChannelNameForm()
                        form2 = ChangeChannelDPForm()
                        form3 = ChangeChannelAboutForm()
                        form4 = ChangeChannelWebsiteForm()
                        context['form']= form
                        context['form2']= form2
                        context['form3']= form3
                        context['form4']= form4
                        context['no_channel']= False
                        context['errors']= errors
                elif request.POST.__contains__('about'):
                    if form3.is_valid():
                        form3.save(pk)
                        return redirect(f'/edit_channel/{pk}')
                    else:
                        errors = check_errors(form3)
                        form = ChangeChannelNameForm()
                        form2 = ChangeChannelDPForm()
                        form3 = ChangeChannelAboutForm()
                        form4 = ChangeChannelWebsiteForm()
                        context['form']= form
                        context['form2']= form2
                        context['form3']= form3
                        context['form4']= form4
                        context['errors']= errors            
                elif request.POST.__contains__('website_official'):
                    if form4.is_valid():
                        form4.save(pk)
                        return redirect(f'/edit_channel/{pk}')
                    else:
                        errors = check_errors(form3)
                        form = ChangeChannelNameForm()
                        form2 = ChangeChannelDPForm()
                        form3 = ChangeChannelAboutForm()
                        form4 = ChangeChannelWebsiteForm()
                        context['form']= form
                        context['form2']= form2
                        context['form3']= form3
                        context['form4']= form4
                        context['errors']= errors            
                else:
                    form = ChangeChannelNameForm()
                    form2 = ChangeChannelDPForm()
                    form3 = ChangeChannelAboutForm()
                    form4 = ChangeChannelWebsiteForm()
                    context['form']= form
                    context['form2']= form2
                    context['form3']= form3
                    context['form4']= form4

            else:
                form = ChangeChannelNameForm()
                form2 = ChangeChannelDPForm()
                form3 = ChangeChannelAboutForm()
                form4 = ChangeChannelWebsiteForm()
                context['form']= form
                context['form2']= form2
                context['form3']= form3
                context['form4']= form4
            return render(request, 'registration/edit_channel.html', context)
        else:
            return HttpResponseForbidden("You don't Own this Channel")
    else:
        return redirect('login')
