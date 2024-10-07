from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.db.models import F
from .models import Choice, Question
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Profile
def index(request):
    return render(request, "index.html")

def signup(request):
    return render(request, "registration/signup.html")
def forgot_password(request):
    return render(request, 'forgotpassword.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        print(f"Attempting to log in user: {username}")
        print(f"User authenticated: {user is not None}")  # This will print True if authenticated successfully

        if user is not None:
            login(request, user)  # Log the user in
            return redirect('mapview')  # Redirect to profile after login
        else:
            # Return an 'invalid login' message
            pass
    return render(request, 'registration/login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return render(request, 'registration/signup.html')

        # Create a new user
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()

        # Check if the profile already exists for the user
        if Profile.objects.filter(user=user).exists():
            messages.warning(request, "Profile already exists for this user.")
            # Redirect to the profile page or some other appropriate action
            return redirect('mapview')  # Change to your desired redirect URL

        # Create a profile for the user
        profile = Profile.objects.create(user=user)
        profile.save()

        # Automatically log in the user after signup
        login(request, user)
        return redirect('mapview')  # Redirect to the profile page after signup

    return render(request, 'registration/signup.html')
def mapview(request):
    return render(request, 'mapview.html')  # Ensure this template exists
@login_required
def profile_view(request):
    user = request.user  # Access the logged-in user
    return render(request, 'user/profile.html', {
        'user': user,  # Pass user object to the template
    })