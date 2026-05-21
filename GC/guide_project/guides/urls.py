from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'guides'

urlpatterns = [
    #Вход
    path('', auth_views.LoginView.as_view(template_name='guides/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Регистрация
    path('register/', views.register, name='register'),
    # Главная стараница
    path('home/', views.home, name='home'),
    # Список стран
    path('country/', views.country_list, name='country_list'),
    # Добавление стран
    path('country/create/', views.country_create, name='country_create'),
    # Удаление трассы
    path('country/<int:pk>/delete/', views.country_delete, name='country_delete'),
    # Добавление поездки с бюджетом
    path('trip/create/', views.trip_create, name='trip_create'),
]