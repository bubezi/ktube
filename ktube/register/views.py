from django.shortcuts import render, redirect
from .forms import UserSignUpForm, ChangeUserDetailsForm, ChannelForm as ChannelCreationForm
from django.contrib.auth import authenticate, login
from .myFunctions import check_errors
from tube.models import Viewer



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
    customer = request.user.customer
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ChangeUserDetailsForm(request.POST, request.FILES, instance=customer)
            if form.is_valid():
                form.save()
                return render(request, "registration/profile.html", context={'customer': customer, "form": form})
            else:
                errors = check_errors(form)
                form = ChangeUserDetailsForm(request.POST, request.FILES, instance=customer)
                context = {'customer': customer, "form": form, "errors": errors}

        else:
            form = ChangeUserDetailsForm()
            context = {'customer': customer, "form": form}
        return render(request, "registration/profile.html", context)
    else:
        return redirect('login')
    
    
def create_channel(request, pk):
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
