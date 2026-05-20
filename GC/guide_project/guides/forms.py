from django import forms
from .models import Country
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Trip
from .models import Budget

# Форма для стран
class CountryForm(forms.ModelForm):

    class Meta:
        model = Country
        fields = ['name', 'currency', 'vat_rate', 'language']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название страны'
            }),

            'currency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Валюта'
            }),

            'vat_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Налоговая ставка)'
            }),

            'language': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Язык'
            })
        }

# Форма для пользователя
class UsersForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем стили (опционально)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Имя'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Фамилия'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Подтвердите пароль'})

#Форма для поездок
class TripForm(forms.ModelForm):

    class Meta:
        model = Trip
        fields = ['сountry', 'user', 'start_date', 'end_date']
        widgets = {
           'сountry': forms.Select(attrs={
                'class': 'form-control' 
            }),

            'user': forms.Select(attrs={
                'class': 'form-control' 
            }),

            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': '2026-05-20'
            }),

            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': '2026-06-20'
            }),
        }

# Форма пользователя бюджета
class BudgetForm(forms.ModelForm):

    class Meta:
        model = Budget
        fields = ['trip', 'amount', 'daily_limit', 'threshold_limit', 'spent']
        widgets = {
           'trip': forms.Select(attrs={
                'class': 'form-control' 
            }),

            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '100000'
            }),

            'daily_limit': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1000'
            }),

            'threshold_limit': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),

            'spent': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '900'
            }),
        }
