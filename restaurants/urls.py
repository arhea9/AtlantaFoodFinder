from django.urls import path

from restaurants import views

app_name = "restaurants"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
]