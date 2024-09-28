import requests  # Ensure this is at the top of your views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework import viewsets
from .serializers import RestaurantSerializer
from django.conf import settings
from .models import Restaurant
import math
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.contrib.auth import login

GOOGLE_MAPS_API_KEY = 'AIzaSyD5MEhM_JZWoMAyUrWAbDSX8ATypigqRHI'

def index(request):
    return render(request, "restaurants/index.html")

from django.contrib.auth import login
from .forms import SignUpForm  # Import your SignUpForm

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm  # Import your SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in after successful registration
            return redirect('map')  # Redirect to the map page after registration
        else:
            # Debugging: Print form errors to the console
            print(form.errors)  # This will show any validation errors in the console
    else:
        form = SignUpForm()

    return render(request, 'restaurants/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is None:
                print("User is None. Check form validation or user retrieval.")
            login(request, user)  # Log the user in
            return redirect('map')  # Redirect to the map page
    else:
        form = AuthenticationForm()
    return render(request, 'restaurants/login.html', {'form': form})

def haversine(lat1, lon1, lat2, lon2):
    # Radius of Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Difference in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c  # Output distance in kilometers
    return distance

def map_view(request):
    query = request.GET.get('query', '')
    cuisine = request.GET.get('cuisine', '')  # User-provided cuisine type
    location = request.GET.get('location', '')  # User-provided location
    min_rating = request.GET.get('min_rating', '0')  # Default min rating
    max_distance = request.GET.get('max_distance', '3')  # Default to 3km

    try:
        min_rating = float(min_rating)
    except ValueError:
        min_rating = 0

    try:
        max_distance = float(max_distance)
    except ValueError:
        max_distance = 3  # Default to 3km if input is invalid

    # If location is not provided, default to user's location or Scheller College
    if not location:
        user_latitude = 33.776389  # Scheller College default latitude
        user_longitude = -84.3875  # Scheller College default longitude
    else:
        # Geocode the location
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={settings.GOOGLE_MAPS_API_KEY}"
        geocode_response = requests.get(geocode_url).json()

        if geocode_response['status'] == 'OK' and geocode_response['results']:
            lat_lng = geocode_response['results'][0]['geometry']['location']
            user_latitude = lat_lng['lat']
            user_longitude = lat_lng['lng']
        else:
            # Fallback to default location (Scheller College of Business)
            user_latitude = 33.776389
            user_longitude = -84.3875

    # Search for places
    google_places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'key': settings.GOOGLE_MAPS_API_KEY,
        'keyword': query + ' ' + cuisine,  # Combine query and cuisine for filtering
        'type': 'restaurant',
        'location': f"{user_latitude},{user_longitude}",
        'radius': max_distance * 1000,  # Radius in meters (default 3km)
    }

    response = requests.get(google_places_url, params=params)
    places_data = response.json()

    # Filter results based on rating
    filtered_restaurants = []
    if places_data.get('results'):
        for restaurant in places_data['results']:
            if restaurant.get('rating', 0) >= min_rating:
                filtered_restaurants.append({
                    'name': restaurant['name'],
                    'latitude': restaurant['geometry']['location']['lat'],
                    'longitude': restaurant['geometry']['location']['lng'],
                    'rating': restaurant.get('rating', 'No rating'),
                    'address': restaurant.get('vicinity'),
                    'place_id': restaurant.get('place_id')  # Add place_id for details
                })

    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'restaurants': filtered_restaurants,
        'user_latitude': user_latitude,
        'user_longitude': user_longitude,
    }

    return render(request, 'restaurants/map.html', context)

def forgot_password(request):
    return render(request, 'restaurants/forgotpassword.html')

# views.py

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomPasswordResetForm


def custom_password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            new_password = form.cleaned_data.get('new_password')

            try:
                user = User.objects.get(email=email)
                user.password = make_password(new_password)
                user.save()
                messages.success(request, 'Your password has been updated successfully.')
                return redirect('login')  # Redirect to login after success
            except User.DoesNotExist:
                messages.error(request, 'No user found with that email address.')
    else:
        form = CustomPasswordResetForm()

    return render(request, 'restaurants/password_reset.html', {'form': form})

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
    success_url = reverse_lazy('index')  # Redirect to homepage (index.html)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

