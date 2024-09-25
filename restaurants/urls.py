from django.urls import path
from django.contrib import admin
from django.urls import include, path
from restaurants import views

app_name = "restaurants"
urlpatterns = [
path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Include Django's auth URLs
    path('', include('restaurants.urls')),  # Adjust this to your app name
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('forgotpassword/', views.forgot_password, name='forgot_password'),
    path('submit_login/', views.login_view, name='submit_login'),
    path('mapview/', views.mapview, name='mapview'),  # This renders mapview.html
    path('profile/', views.profile_view, name='profile_page'),
]