from django.urls import path

from restaurants import views

app_name = "restaurants"
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('forgotpassword/', views.forgot_password, name='forgot_password'),
    path('submit_login/', views.login_view, name='submit_login'),
    path('mapview/', views.mapview, name='mapview'),  # This renders mapview.html
]