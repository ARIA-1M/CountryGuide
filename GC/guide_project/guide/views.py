from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CountryForm



def home(request):
    return render(request, 'guides/home.html')

# Добавление новой трассы
def country_create(request):
    if request.method == 'POST':
        form = CountryForm(request.POST, request.FILES)
        if form.is_valid():
            country = form.save()
            messages.success(request, f'Страна "{country.name}" успешно добавлена!')
            return redirect('guide:home')
    else:
        form = CountryForm()
    
    return render(request, 'guide/country_create.html', {
        'form': form, 'title': 'Добавить страну'
    })