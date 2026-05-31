from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Country

class CountryListViewTest(TestCase):# Тестирование просмотра списка стран

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        self.client.force_login(self.user)
        
        Country.objects.create(name='Мексика', currency='MXN', vat_rate=6.00, language='Испанский')
        Country.objects.create(name='Бразилия', currency='BRL', vat_rate=7.00, language='Португальский')
        Country.objects.create(name='Дания', currency='DKK', vat_rate=5.00, language='Датский')
        Country.objects.create(name='Япония', currency='JPY', vat_rate=8.00, language='Японский')
        Country.objects.create(name='Марокко', currency='MAD', vat_rate=2.00, language='Арабский')
        Country.objects.create(name='Австралия', currency='AUD', vat_rate=5.00, language='Английский')

    def test_country_list_view_contains_countries(self):# Проверка на наличие стран
        response = self.client.get(reverse('guides:country_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Мексика')
        self.assertContains(response, 'Бразилия')
        self.assertContains(response, 'Дания')
        self.assertContains(response, 'Япония')
        self.assertContains(response, 'Марокко')
        self.assertContains(response, 'Австралия')

    def test_country_list_view_count(self):# Проверка на количество стран
        response = self.client.get(reverse('guides:country_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['countries']), 6)


class CountryCreateTest(TestCase):# Тестирование добавления страны

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        self.client.force_login(self.admin_user)

    def test_create_country_post_valid_data(self):# Проверка на добавления стран с корректными данными 
        response = self.client.post(reverse('guides:country_create'), {
            'name': 'Канада',
            'currency': 'CAD',
            'vat_rate': 5.00,
            'language': 'Английский'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Country.objects.count(), 1)
        self.assertTrue(Country.objects.filter(name='Канада').exists())

    def test_create_country_post_invalid_data(self):# Проверка добавления страны с некорректными данными 
        response = self.client.post(reverse('guides:country_create'), {
            'name': '',
            'currency': 'EGP',
            'vat_rate': 5.00,
            'language': 'Арабский'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Country.objects.count(), 0)


class CountryDeleteTest(TestCase):# Тестирование удаления страны

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        self.client.force_login(self.admin_user)
        self.country = Country.objects.create(
            name='Таиланд',
            currency='THB',
            vat_rate=7.00,
            language='Тайский'
        )

    def test_delete_country_with_admin_login(self):# Удаление существующей страны 
        response = self.client.post(reverse('guides:country_delete', args=[self.country.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Country.objects.filter(id=self.country.id).exists())

    def test_delete_nonexistent_country(self):# Удаления несуществующей страны
        response = self.client.post(reverse('guides:country_delete', args=[999]))
        self.assertEqual(response.status_code, 404)
