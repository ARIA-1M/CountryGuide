from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CountryForm
from .models import Country, Article, LocalApp, PhraseCategory, Phrase


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

def phrases_list(request):
    countries = Country.objects.all()
    selected_country_id = request.GET.get('country_id')
    selected_category_id = request.GET.get('category_id')
    categories = None
    phrases = None
    selected_country = None
    selected_category = None
    
    if selected_country_id:
        selected_country = get_object_or_404(Country, id=selected_country_id)
        # Получаем категории, у которых есть фразы для этой страны
        categories = PhraseCategory.objects.filter(phrase__country=selected_country).distinct()
    
    if selected_category_id and selected_country_id:
        selected_category = get_object_or_404(PhraseCategory, id=selected_category_id)
        # Получаем фразы выбранной категории для выбранной страны
        phrases = Phrase.objects.filter(
            category=selected_category, 
            country=selected_country
        )
    
    return render(request, 'guides/phrases_list.html', {
        'countries': countries,
        'selected_country_id': selected_country_id,
        'selected_category_id': selected_category_id,
        'categories': categories,
        'phrases': phrases,
        'selected_country': selected_country,
        'selected_category': selected_category,
    })