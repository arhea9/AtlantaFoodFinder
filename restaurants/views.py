from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import F
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Choice, Question

def index(request):
    return render(request, "restaurants/index.html")

def signup(request):
    return render(request, "restaurants/signup.html")

def login(request):
    return render(request, "restaurants/login.html")

def forgot_password(request):
    return render(request, "restaurants/forgotpassword.html")

def login_view(request):
    if request.method == 'POST':
        # Process the login form (authentication, etc.)
        # Assuming successful login:
        return redirect('mapview')  # Use the URL name
    return render(request, 'restaurants/login.html')  # Redirect back to the login page if GET

def signup_view(request):
    if request.method == 'POST':
        # Process the signup form
        # Here, you would validate and save the user data
        # If successful, redirect to the mapview
        return redirect('mapview')  # Redirect to mapview after successful signup
    return render(request, 'restaurants/signup.html')  # Render the signup page on GET

@login_required
def profile_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'restaurants/profile.html', {'profile_page': profile})  # Ensure this template exists

def mapview(request):
    return render(request, 'restaurants/mapview.html')  # Ensure this template exists
