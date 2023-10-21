from django.shortcuts import render

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from .Forms import *

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)# Log in the user after registration
            if (user_has_completed_form(user)):
                return render(request, 'orderScreen.html')
                # Redirect to a success page or the home page
            else:
                return render(request, 'path_to_template.html')  # Replace 'home' with your desired URL name
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if (user_has_completed_form(user)):
                    return render(request, 'orderScreen.html')
                # Redirect to a success page or the home page
                else:
                    return render(request, 'path_to_template.html')
            else:
                # User does not exist, provide a sign-up option
                return render(request, 'signup.html')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



def profile_update(request):
    try:
        instance = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        instance = None

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=instance)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return HttpResponseRedirect(reverse('profile_update'))
    else:
        form = UserProfileForm(instance=instance)

    return render(request, 'path_to_template.html', {'form': form})


def user_has_completed_form(user):
    """
    Check if the user has completed the user profile form.
    Returns True if the form is complete, False otherwise.
    """
    try:
        profile = UserProfile.objects.get(user=user)
        # Check if the required fields are not empty
        if profile.first_name and profile.last_name and profile.meal_plan and profile.current_dining_dollars:
            return True
    except UserProfile.DoesNotExist:
        pass

    return False

