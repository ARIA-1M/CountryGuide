from django.shortcuts import render, redirect, get_object_or_404
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


# Главная страница
def home(request):
    return render(request, 'guides/home.html')

# Список стран
def country_list(request):
    countries = Country.objects.all()
    return render(request, 'guides/country_list.html', {'countries': countries})

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

# Страница бюджета активной поездки
def trip_budget(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    budget = Budget.objects.get(trip=trip)
    
    return render(request, 'guides/trip_budget.html', { 
        'trip': trip,
        'budget': budget,
    })

# Нахождение актуально бюджета
def latest_budget(request):
    trip = Trip.objects.filter(user=request.user, is_active=True).first()
    if not trip:
        return redirect('guides:trip_create')
    return redirect('guides:trip_budget', trip_id=trip.id)  

# Завершение поездки
def complete_trip(request, trip_id):
    if request.method == 'POST':
        trip = get_object_or_404(Trip, id=trip_id, user=request.user)
        trip.is_active = False
        trip.save()
        messages.success(request, 'Поездка завершена!')
        return redirect('guides:home')
    return redirect('guides:trip_budget', trip_id=trip_id)

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