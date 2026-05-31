from django.shortcuts import render, redirect, get_object_or_404
from .models import Country, Article, LocalApp, PhraseCategory, Phrase
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CountryForm
from .forms import TripBudgetForm
from .models import Country
from .models import Budget
from .models import Trip
from .forms import UsersForm
import json
from django.http import JsonResponse
from decimal import Decimal
from .forms import TripBudgetForm
from .forms import UsersForm


def is_admin(user):
    return user.is_staff or user.is_superuser


# Главная страница
def home(request):
    return render(request, 'guides/home.html')


@user_passes_test(is_admin)
# Список стран
def country_list(request):
    countries = Country.objects.all()
    return render(request, 'guides/country_list.html', {'countries': countries})


@user_passes_test(is_admin)
# Добавление новой страны 
def country_create(request):
    if request.method == 'POST':
        form = CountryForm(request.POST)
        print(form.errors)  
        if form.is_valid():
            form.save()
            return redirect('/country/')
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


@user_passes_test(is_admin)
# Удаление страны
def country_delete(request, pk):
    country = get_object_or_404(Country, pk=pk)
    
    if request.method == 'POST':
        country_name = country.name
        country.delete()
        messages.success(request, f'Трасса "{country_name}" удалена!')
        return redirect('/country/')
    
    return render(request, 'guides/country_confirm_delete.html', {'country': country})

# Регистрация
def register(request):
    if request.method == 'POST':
        form = UsersForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
            return redirect('/')
        else:
            print(form.errors) 
    else:
        form = UsersForm()
    
    return render(request, 'guides/register.html', {'form': form})

@login_required
# Создание поездки
def trip_create(request):
    if request.method == 'POST':
        form = TripBudgetForm(request.POST)
        if form.is_valid():
            trip = form.save(user=request.user)
            messages.success(request, f'Поездка в {trip.сountry.name} успешно создана!')
            return redirect('guides:home')
    else:
        form = TripBudgetForm()


    
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
@login_required
@user_passes_test(is_admin)
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

@login_required
@user_passes_test(is_admin)
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

@login_required
@user_passes_test(is_admin)
def article_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Статья удалена')
        return redirect('guides:articles_list')
    return render(request, 'guides/confirm_delete.html', {'object': article, 'type': 'статью'})


# ==================== CRUD для приложений ====================
@login_required
@user_passes_test(is_admin)
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

@login_required
@user_passes_test(is_admin)
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

@login_required
@user_passes_test(is_admin)
def app_delete(request, app_id):
    app = get_object_or_404(LocalApp, id=app_id)
    if request.method == 'POST':
        app.delete()
        messages.success(request, 'Приложение удалено')
        return redirect('guides:articles_list')
    return render(request, 'guides/confirm_delete.html', {'object': app, 'type': 'приложение'})


# ==================== CRUD для категорий фраз ====================
@login_required
@user_passes_test(is_admin)
def category_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        PhraseCategory.objects.create(title=title)
        messages.success(request, 'Категория добавлена')
        return redirect('guides:phrases_list')
    return render(request, 'guides/category_form.html', {'mode': 'create'})

@login_required
@user_passes_test(is_admin)
def category_edit(request, category_id):
    category = get_object_or_404(PhraseCategory, id=category_id)
    if request.method == 'POST':
        category.title = request.POST.get('title')
        category.save()
        messages.success(request, 'Категория обновлена')
        return redirect('guides:phrases_list')
    return render(request, 'guides/category_form.html', {'category': category, 'mode': 'edit'})

@login_required
@user_passes_test(is_admin)
def category_delete(request, category_id):
    category = get_object_or_404(PhraseCategory, id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Категория удалена')
        return redirect('guides:phrases_list')
    return render(request, 'guides/confirm_delete.html', {'object': category, 'type': 'категорию'})


# ==================== CRUD для фраз ====================
@login_required
@user_passes_test(is_admin)
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

@login_required
@user_passes_test(is_admin)
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

@login_required
@user_passes_test(is_admin)
def phrase_delete(request, phrase_id):
    phrase = get_object_or_404(Phrase, id=phrase_id)
    if request.method == 'POST':
        phrase.delete()
        messages.success(request, 'Фраза удалена')
        return redirect('guides:phrases_list')
    return render(request, 'guides/confirm_delete.html', {'object': phrase, 'type': 'фразу'})
@login_required
# Создание поездки
def trip_create(request):
    if request.method == 'POST':
        form = TripBudgetForm(request.POST)
        if form.is_valid():
            Trip.objects.filter(user=request.user, is_active=True).update(is_active=False)
            trip = form.save(user=request.user)
            trip.is_active = True
            trip.save()
            return redirect('guides:trip_budget', trip_id=trip.id)
    else:
        form = TripBudgetForm()
    
    return render(request, 'guides/trip_create.html', {'form': form, 'title': 'Создать поездку'})
            
@login_required
# Страница бюджета активной поездки
def trip_budget(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    budget = Budget.objects.get(trip=trip)
    
    return render(request, 'guides/trip_budget.html', { 
        'trip': trip,
        'budget': budget,
    })

@login_required
# Редактирование поездки
def trip_edit(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    budget = Budget.objects.get(trip=trip)
    
    if request.method == 'POST':
        form = TripBudgetForm(request.POST, instance=trip)
        if form.is_valid():
            # Обновляем поездку вручную (без form.save)
            trip.country = form.cleaned_data['country']
            trip.start_date = form.cleaned_data['start_date']
            trip.end_date = form.cleaned_data['end_date']
            trip.save()
            
            # Обновляем бюджет
            budget.amount = form.cleaned_data['amount']
            budget.daily_limit = form.cleaned_data['daily_limit']
            budget.threshold_limit = form.cleaned_data['threshold_limit']
            budget.save()
            
            return redirect('guides:trip_budget', trip_id=trip.id)
    else:
        form = TripBudgetForm(instance=trip, initial={
            'amount': budget.amount,
            'daily_limit': budget.daily_limit,
            'threshold_limit': budget.threshold_limit,
        })
    
    return render(request, 'guides/trip_create.html', {
        'form': form, 
        'title': 'Редактировать поездку'
    })

@login_required
# Нахождение актуально бюджета
def latest_budget(request):
    trip = Trip.objects.filter(user=request.user, is_active=True).first()
    if not trip:
        return redirect('guides:trip_create')
    return redirect('guides:trip_budget', trip_id=trip.id)  

@login_required
# Завершение поездки
def complete_trip(request, trip_id):
    if request.method == 'POST':
        trip = get_object_or_404(Trip, id=trip_id, user=request.user)
        trip.is_active = False
        trip.save()
        messages.success(request, 'Поездка завершена!')
        return redirect('guides:home')
    return redirect('guides:trip_budget', trip_id=trip_id)

@login_required
# Обработка обновлнеи
def api_add_expense(request, trip_id):  
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount_rub = Decimal(str(data.get('amount_rub', 0)))
            amount_local = Decimal(str(data.get('amount_local', 0)))
            include_tax = data.get('include_tax', False)
            
            trip = get_object_or_404(Trip, id=trip_id, user=request.user)
            budget = Budget.objects.get(trip=trip)
            
            budget.spent += amount_rub
            budget.save()
            
            remaining = budget.amount - budget.spent
            
            return JsonResponse({
                'success': True,
                'new_spent': float(budget.spent),
                'remaining': float(remaining)
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid method'})

# Завершение поездки через кнопку
@login_required
def api_complete_trip(request, trip_id): 
    if request.method == 'POST':
        try:
            trip = get_object_or_404(Trip, id=trip_id, user=request.user)
            if not trip.is_active:
                return JsonResponse({'success': False, 'error': 'Поездка уже завершена'})
        
            trip.is_active = False
            trip.save()
            messages.success(request, f'Поездка в {trip.country.name} завершена!')
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid method'})

