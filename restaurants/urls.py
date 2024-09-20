from django.urls import path
from restaurants import views
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)

app_name = "restaurants"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('map/', views.map_view, name='map'),
    path('api/', include(router.urls)),
]