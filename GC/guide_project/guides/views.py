from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CountryForm
from .forms import TripBudgetForm
from .models import Country
from .models import Budget
from .models import Trip
from .forms import UsersForm


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
            return redirect('guides:budget_detail', trip_id=trip.id)
    else:
        form = TripBudgetForm()
    
    return render(request, 'guides/trip_create.html', {'form': form, 'title': 'Создать поездку'})

# Страница бюджета активной поездки
def trip_budget(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    budget = Budget.objects.get(trip=trip)
    
    return render(request, 'guides/trip_budget.html', {  # ← имя шаблона
        'trip': trip,
        'budget': budget,
    })

# Нахождение актуально бюджета
def latest_budget(request):
    trip = Trip.objects.filter(user=request.user, is_active=True).first()
    if not trip:
        return redirect('guides:trip_create')
    return redirect('guides:trip_budget', trip_id=trip.id)  # ← исправлено

# Завершение поездки
def complete_trip(request, trip_id):
    if request.method == 'POST':
        trip = get_object_or_404(Trip, id=trip_id, user=request.user)
        trip.is_active = False
        trip.save()
        messages.success(request, 'Поездка завершена!')
        return redirect('guides:home')
    return redirect('guides:trip_budget', trip_id=trip_id)

def api_add_expense(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            trip_id = data.get('trip_id')
            amount_rub = data.get('amount_rub')
            
            trip = get_object_or_404(Trip, id=trip_id, user=request.user)
            budget = Budget.objects.get(trip=trip)
            
            budget.spent += amount_rub
            budget.save()
            
            return JsonResponse({
                'success': True,
                'new_spent': float(budget.spent),
                'remaining': float(budget.remaining)
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid method'})


def api_complete_trip(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            trip_id = data.get('trip_id')
            
            trip = get_object_or_404(Trip, id=trip_id, user=request.user)
            trip.is_active = False
            trip.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid method'})