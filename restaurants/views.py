from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import F
from .models import Choice, Question
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework import viewsets
from .serializers import RestaurantSerializer
from django.conf import settings
from django.shortcuts import render
from .models import Restaurant
import math
import requests
from django.shortcuts import render

GOOGLE_MAPS_API_KEY = 'AIzaSyD5MEhM_JZWoMAyUrWAbDSX8ATypigqRHI'

def index(request):
    return render(request, "restaurants/index.html")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in after successful registration
            return redirect('map')  # Redirect to the map page after registration
    else:
        form = UserCreationForm()
    return render(request, 'restaurants/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
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


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
