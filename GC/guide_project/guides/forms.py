from django import forms
from .models import Country
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Форма для создания стран
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

#Форма для создания пользователя
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
