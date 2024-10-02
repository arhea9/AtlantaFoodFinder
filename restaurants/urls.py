from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from restaurants import views

app_name = "restaurants"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('submit_signup/', views.signup_view, name='submit_signup'),  # Handle form submission
    path('login/', views.login, name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('forgotpassword/', views.forgot_password, name='forgot_password'),
    path('submit_login/', views.login_view, name='submit_login'),  
    path('mapview/', views.mapview, name='mapview'),  # This renders mapview.html
    path('profile/', views.profile_view, name='profile'),  # This renders profile.html
    path('index/', views.index, name='index'),  # This renders profile.html

]