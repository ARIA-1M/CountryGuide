from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CountryForm
from .models import Country
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
            return redirect('guides/home')
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
        return redirect('guides/home')
    
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
            trip = form.save(user=request.user)
            messages.success(request, f'Поездка в {trip.сountry.name} успешно создана!')
            return redirect('guides:trip_list')
    else:
        form = TripBudgetForm()
    
    return render(request, 'guides/trip_create.html', {'form': form, 'title': 'Создать поездку'})