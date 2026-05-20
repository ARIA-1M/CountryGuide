from django import forms
from .models import Country

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