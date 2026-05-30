from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.contrib.auth import views as auth_views


app_name = 'guides'

urlpatterns = [

    path('country/<int:country_id>/', views.country_detail, name='country_detail'),
    path('articles/', views.articles_list, name='articles_list'),
    path('phrases/', views.phrases_list, name='phrases_list'),

     # Статьи
    path('article/create/', views.article_create, name='article_create'),
    path('article/edit/<int:article_id>/', views.article_edit, name='article_edit'),
    path('article/delete/<int:article_id>/', views.article_delete, name='article_delete'),
    
    # Приложения
    path('app/create/', views.app_create, name='app_create'),
    path('app/edit/<int:app_id>/', views.app_edit, name='app_edit'),
    path('app/delete/<int:app_id>/', views.app_delete, name='app_delete'),
    
    # Категории фраз
    path('category/create/', views.category_create, name='category_create'),
    path('category/edit/<int:category_id>/', views.category_edit, name='category_edit'),
    path('category/delete/<int:category_id>/', views.category_delete, name='category_delete'),
    
    # Фразы
    path('phrase/create/', views.phrase_create, name='phrase_create'),
    path('phrase/edit/<int:phrase_id>/', views.phrase_edit, name='phrase_edit'),
    path('phrase/delete/<int:phrase_id>/', views.phrase_delete, name='phrase_delete'),


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