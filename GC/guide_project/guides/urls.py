from django.urls import path
from . import views

app_name = 'guides'

urlpatterns = [
    path('', views.home, name='home'),
    path('country_create/', views.country_create, name='country_create'),
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
]