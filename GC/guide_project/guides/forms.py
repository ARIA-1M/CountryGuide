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

# Форма для создания бюджета с поездкой
class TripBudgetForm(forms.ModelForm):
    # Поля бюджета
    amount = forms.DecimalField(
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Общий бюджет'})
    )
    daily_limit = forms.DecimalField(
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Лимит на день'})
    )
    threshold_limit = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Trip
        fields = ['country', 'start_date', 'end_date']
        widgets = {
            'country': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def save(self, user, commit=True):
        # Создаём поездку
        trip = super().save(commit=False)
        trip.user = user
        if commit:
            trip.save()
            # Создаём бюджет для этой поездки
            Budget.objects.create(
                trip=trip,
                amount=self.cleaned_data['amount'],
                daily_limit=self.cleaned_data['daily_limit'],
                threshold_limit=self.cleaned_data['threshold_limit'],
                spent=0
            )
        return trip