from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CountryForm
from .models import Country, Article


def home(request):
    return render(request, 'guides/home.html')

# Добавление новой страны 
def country_create(request):
    if request.method == 'POST':
        form = CountryForm(request.POST)
        print(form.errors)  
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = CountryForm()
    
    return render(request, 'guides/country_create.html', {'form': form})

def country_detail(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    articles = country.articles.all().order_by('-update')
    return render(request, 'guides/country_detail.html', {
        'country': country,
        'articles': articles,
    }) 


def articles_list(request):
    countries = Country.objects.all()
    selected_country_id = request.GET.get('country_id')
    articles = None
    
    if selected_country_id:
        selected_country = get_object_or_404(Country, id=selected_country_id)
        articles = selected_country.articles.all().order_by('-update')
    else:
        selected_country = None
    
    return render(request, 'guides/articles_list.html', {
        'countries': countries,
        'selected_country_id': int(selected_country_id) if selected_country_id else None,
        'articles': articles,
        'selected_country': selected_country,
    })

def articles_list(request):
    countries = Country.objects.all()
    selected_country_id = request.GET.get('country_id')
    articles = None
    apps = None
    selected_country = None
    
    if selected_country_id:
        selected_country = get_object_or_404(Country, id=selected_country_id)
        articles = selected_country.articles.all().order_by('-update')
        apps = selected_country.apps.all()  # добавляем приложения
    
    return render(request, 'guides/articles_list.html', {
        'countries': countries,
        'selected_country_id': selected_country_id,
        'articles': articles,
        'apps': apps,
        'selected_country': selected_country,
    })