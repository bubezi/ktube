from django.shortcuts import render, redirect
from .forms import UserSignUpForm, ChangePhoneForm, ChangeGenderForm, ChangeChannelForm, ChannelForm as ChannelCreationForm
from django.contrib.auth import authenticate, login
from .myFunctions import check_errors
from tube.models import Viewer, Channel



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
        context={'viewer': viewer}
        try:
            channel = Channel.objects.get(user=viewer)
            context['channel']=channel
            context['nav_channel']=channel
            context['no_channel'] = False
        except Channel.DoesNotExist:
            context['no_channel'] = True
        except:
            context['many_channels'] = True
            context['no_channel'] = True
            
        if request.method == "POST":
            form = ChangePhoneForm(request.POST, request.FILES, instance=viewer)
            form2 = ChangeGenderForm(request.POST, request.FILES, instance=viewer)
            if not request.POST.__contains__('phone'):
                if form2.is_valid:
                    form2.save()
                    return redirect('profile')
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
        if request.method == "POST":
            form = ChannelCreationForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    form.save(pk)
                    return redirect('/')
                except Viewer.DoesNotExist as e:
                    form = ChannelCreationForm()
                    context = {"form": form, "errors": e, "no_channel": True}
            else:
                errors = check_errors(form)
                form = ChannelCreationForm()
                context = {"form": form, "errors": errors, "no_channel": True}

        else:
            form = ChannelCreationForm()
            context = {"form": form, "no_channel": True}
        return render(request, 'registration/create_channel.html', context)
    else:
        return redirect('login')
    

def change_channel_details(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ChangeChannelForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    form.save(pk)
                    return redirect('/')
                except Viewer.DoesNotExist as e:
                    form = ChangeChannelForm()
                    context = {"form": form, "errors": e, "no_channel": True}
            else:
                errors = check_errors(form)
                form = ChangeChannelForm()
                context = {"form": form, "errors": errors, "no_channel": True}

        else:
            form = ChangeChannelForm()
            context = {"form": form, "no_channel": True}
        return render(request, 'registration/change_channel_details.html', context)
    else:
        return redirect('login')
