from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import F
from .models import Choice, Question

def index(request):
    return render(request, "restaurants/index.html")

def signup(request):
    return render(request, "restaurants/signup.html")

def login(request):
    return render(request, "restaurants/login.html")

def forgot_password(request):
    return render(request, 'restaurants/forgotpassword.html')