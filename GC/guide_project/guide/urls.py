from django.urls import path
from . import views

app_name = 'guide'

urlpatterns = [
    path('', views.home, name='home'),
    path('country_create/', views.country_create, name='country_create'),
]