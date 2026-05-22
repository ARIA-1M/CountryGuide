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