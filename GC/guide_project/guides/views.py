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
    apps = None
    selected_country = None
    
    if selected_country_id:
        selected_country = get_object_or_404(Country, id=selected_country_id)
        articles = selected_country.articles.all().order_by('-update')
        apps = selected_country.apps.all()
    
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
        categories = PhraseCategory.objects.filter(phrase__country=selected_country).distinct()
    
    if selected_category_id and selected_country_id:
        selected_category = get_object_or_404(PhraseCategory, id=selected_category_id)
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


# ==================== CRUD для статей ====================

def article_create(request):
    if request.method == 'POST':
        country_id = request.POST.get('country_id')
        title = request.POST.get('title')
        link = request.POST.get('link')
        country = get_object_or_404(Country, id=country_id)
        Article.objects.create(country=country, title=title, link=link)
        messages.success(request, 'Статья добавлена')
        return redirect('guides:articles_list')
    
    countries = Country.objects.all()
    return render(request, 'guides/article_form.html', {'countries': countries, 'mode': 'create'})


def article_edit(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.title = request.POST.get('title')
        article.link = request.POST.get('link')
        article.save()
        messages.success(request, 'Статья обновлена')
        return redirect('guides:articles_list')
    
    countries = Country.objects.all()
    return render(request, 'guides/article_form.html', {
        'article': article,
        'countries': countries,
        'mode': 'edit'
    })


def article_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Статья удалена')
        return redirect('guides:articles_list')
    return render(request, 'guides/confirm_delete.html', {'object': article, 'type': 'статью'})


# ==================== CRUD для приложений ====================

def app_create(request):
    if request.method == 'POST':
        country_id = request.POST.get('country_id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        logo = request.FILES.get('logo')
        country = get_object_or_404(Country, id=country_id)
        LocalApp.objects.create(country=country, title=title, description=description, logo=logo)
        messages.success(request, 'Приложение добавлено')
        return redirect('guides:articles_list')
    
    countries = Country.objects.all()
    return render(request, 'guides/app_form.html', {'countries': countries, 'mode': 'create'})


def app_edit(request, app_id):
    app = get_object_or_404(LocalApp, id=app_id)
    if request.method == 'POST':
        app.title = request.POST.get('title')
        app.description = request.POST.get('description')
        if request.FILES.get('logo'):
            app.logo = request.FILES.get('logo')
        app.save()
        messages.success(request, 'Приложение обновлено')
        return redirect('guides:articles_list')
    
    countries = Country.objects.all()
    return render(request, 'guides/app_form.html', {'app': app, 'countries': countries, 'mode': 'edit'})


def app_delete(request, app_id):
    app = get_object_or_404(LocalApp, id=app_id)
    if request.method == 'POST':
        app.delete()
        messages.success(request, 'Приложение удалено')
        return redirect('guides:articles_list')
    return render(request, 'guides/confirm_delete.html', {'object': app, 'type': 'приложение'})


# ==================== CRUD для категорий фраз ====================

def category_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        PhraseCategory.objects.create(title=title)
        messages.success(request, 'Категория добавлена')
        return redirect('guides:phrases_list')
    return render(request, 'guides/category_form.html', {'mode': 'create'})


def category_edit(request, category_id):
    category = get_object_or_404(PhraseCategory, id=category_id)
    if request.method == 'POST':
        category.title = request.POST.get('title')
        category.save()
        messages.success(request, 'Категория обновлена')
        return redirect('guides:phrases_list')
    return render(request, 'guides/category_form.html', {'category': category, 'mode': 'edit'})


def category_delete(request, category_id):
    category = get_object_or_404(PhraseCategory, id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Категория удалена')
        return redirect('guides:phrases_list')
    return render(request, 'guides/confirm_delete.html', {'object': category, 'type': 'категорию'})


# ==================== CRUD для фраз ====================

def phrase_create(request):
    if request.method == 'POST':
        country_id = request.POST.get('country_id')
        category_id = request.POST.get('category_id')
        original_text = request.POST.get('original_text')
        translated_text = request.POST.get('translated_text')
        transliteration = request.POST.get('transliteration', '')
        country = get_object_or_404(Country, id=country_id)
        category = get_object_or_404(PhraseCategory, id=category_id)
        Phrase.objects.create(
            country=country,
            category=category,
            original_text=original_text,
            translated_text=translated_text,
            transliteration=transliteration
        )
        messages.success(request, 'Фраза добавлена')
        return redirect('guides:phrases_list')
    
    countries = Country.objects.all()
    categories = PhraseCategory.objects.all()
    return render(request, 'guides/phrase_form.html', {
        'countries': countries,
        'categories': categories,
        'mode': 'create'
    })


def phrase_edit(request, phrase_id):
    phrase = get_object_or_404(Phrase, id=phrase_id)
    if request.method == 'POST':
        phrase.original_text = request.POST.get('original_text')
        phrase.translated_text = request.POST.get('translated_text')
        phrase.transliteration = request.POST.get('transliteration', '')
        phrase.save()
        messages.success(request, 'Фраза обновлена')
        return redirect('guides:phrases_list')
    
    countries = Country.objects.all()
    categories = PhraseCategory.objects.all()
    return render(request, 'guides/phrase_form.html', {
        'phrase': phrase,
        'countries': countries,
        'categories': categories,
        'mode': 'edit'
    })


def phrase_delete(request, phrase_id):
    phrase = get_object_or_404(Phrase, id=phrase_id)
    if request.method == 'POST':
        phrase.delete()
        messages.success(request, 'Фраза удалена')
        return redirect('guides:phrases_list')
    return render(request, 'guides/confirm_delete.html', {'object': phrase, 'type': 'фразу'})