from .forms import UserSignUpForm, ChangePhoneForm, ChangeGenderForm, ChangeChannelNameForm, ChangeChannelDPForm, ChangeChannelAboutForm, ChangeChannelWebsiteForm, ChannelForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from tube.models import Viewer, Channel, Watchlater
from .myFunctions import check_errors
from django.http import HttpResponseForbidden, HttpResponseBadRequest


# Create your views here.
def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = UserSignUpForm(request.POST, request.FILES)
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
        watchlater = Watchlater.objects.get(viewer=viewer)
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
    
    
def create_channel(request, pk):
    if request.user.is_authenticated:
        try:
            pk_viewer = Viewer.objects.get(id=pk)
        except Viewer.DoesNotExist as e:
            return HttpResponseBadRequest(e)
        
        viewer = request.user.viewer
        
        owner = False
        if viewer == pk_viewer:
            owner = True
        
        if owner:
            if request.method == "POST":
                form = ChannelForm(request.POST, request.FILES)
                if form.is_valid():
                    try:
                        form.save(pk)
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
            return HttpResponseBadRequest("You cannot create a channel for this User. Click the create channel link on your profile Page.")        

    else:
        return redirect('login')
    

def change_channel_details(request, pk):
    if request.user.is_authenticated:
        viewer = request.user.viewer
        context={'viewer': viewer}
        try:
            channel = Channel.objects.get(id=pk)
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
                        return redirect(f'/change_channel_details/{pk}')
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
                        return redirect(f'/change_channel_details/{pk}')
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
                        return redirect(f'/change_channel_details/{pk}')
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
                        return redirect(f'/change_channel_details/{pk}')
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
            return render(request, 'registration/change_channel_details.html', context)
        else:
            return HttpResponseForbidden("You don't Own this Channel")
    else:
        return redirect('login')
