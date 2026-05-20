from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CountryForm
from .forms import UsersForm



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