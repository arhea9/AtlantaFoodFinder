from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet
from django.contrib.auth import views as auth_views
from django.urls import path
from restaurants import views

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)

app_name = "restaurants"
urlpatterns = [
    path('password_reset/', views.custom_password_reset, name='custom_password_reset'),
    path("", views.index, name="index"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('map/', views.map_view, name='map'),
    path('api/', include(router.urls)),
    path('forgotpassword/', views.forgot_password, name='forgot_password'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]