from django.urls import path
from . import views

app_name = 'guides'

urlpatterns = [
    path('', views.home, name='home'),
    path('country_create/', views.country_create, name='country_create'),
    path('country/<int:country_id>/', views.country_detail, name='country_detail'),
]