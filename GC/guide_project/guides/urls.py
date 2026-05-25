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
    # Добавление поездки
    path('budget/', views.latest_budget, name='budget'),
    path('trip/<int:trip_id>/budget/', views.trip_budget, name='trip_budget'),
    path('trip/<int:trip_id>/complete/', views.complete_trip, name='complete_trip'),
    path('api/add-expense/<int:trip_id>/', views.api_add_expense, name='api_add_expense'),
    path('api/complete-trip/<int:trip_id>/', views.api_complete_trip, name='api_complete_trip'),
    
]