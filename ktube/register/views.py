from django.shortcuts import render, redirect
from .forms import UserSignUpForm, ChangeUserDetailsForm
from django.contrib.auth import authenticate, login
# from django.contrib.sites.models import Site
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.http import HttpResponseBadRequest
from .myFunctions import check_errors



# Create your views here.
def register(request):
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
