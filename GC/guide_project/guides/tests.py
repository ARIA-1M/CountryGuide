import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guide_project.settings')
django.setup()

from django.test import TestCase
from django.urls import reverse
from .models import Country, Article, LocalApp, PhraseCategory, Phrase


class ArticleModelTest(TestCase):
    """Тесты для модели Article"""
    
    def setUp(self):
        self.country = Country.objects.create(
            name='Франция',
            currency='Евро',
            vat_rate=20.0,
            language='Французский'
        )
    
    def test_create_article(self):
        """Тест создания статьи"""
        article = Article.objects.create(
            country=self.country,
            title='Тестовая статья',
            link='https://example.com/test'
        )
        self.assertEqual(article.title, 'Тестовая статья')
        self.assertEqual(article.link, 'https://example.com/test')
        self.assertEqual(article.country.name, 'Франция')
    
    def test_article_str_method(self):
        """Тест строкового представления статьи"""
        article = Article.objects.create(
            country=self.country,
            title='Заголовок',
            link='https://example.com'
        )
        self.assertEqual(str(article), 'Заголовок')
    
    def test_article_update_auto(self):
        """Тест автоматического обновления даты"""
        article = Article.objects.create(
            country=self.country,
            title='Статья',
            link='https://example.com'
        )
        self.assertIsNotNone(article.update)


class LocalAppModelTest(TestCase):
    """Тесты для модели LocalApp"""
    
    def setUp(self):
        self.country = Country.objects.create(
            name='Италия',
            currency='Евро',
            vat_rate=22.0,
            language='Итальянский'
        )
    
    def test_create_app(self):
        """Тест создания приложения"""
        app = LocalApp.objects.create(
            country=self.country,
            title='Google Maps',
            description='Навигационное приложение'
        )
        self.assertEqual(app.title, 'Google Maps')
        self.assertEqual(app.description, 'Навигационное приложение')
        self.assertEqual(app.country.name, 'Италия')
    
    def test_app_str_method(self):
        """Тест строкового представления приложения"""
        app = LocalApp.objects.create(
            country=self.country,
            title='Uber',
            description='Такси'
        )
        self.assertEqual(str(app), 'Uber')


class PhraseCategoryModelTest(TestCase):
    """Тесты для модели PhraseCategory"""
    
    def test_create_category(self):
        """Тест создания категории фраз"""
        category = PhraseCategory.objects.create(title='Приветствия')
        self.assertEqual(category.title, 'Приветствия')
    
    def test_category_str_method(self):
        """Тест строкового представления категории"""
        category = PhraseCategory.objects.create(title='Еда')
        self.assertEqual(str(category), 'Еда')
    
    def test_category_update_auto(self):
        """Тест автоматического обновления даты"""
        category = PhraseCategory.objects.create(title='Транспорт')
        self.assertIsNotNone(category.update)


class PhraseModelTest(TestCase):
    """Тесты для модели Phrase"""
    
    def setUp(self):
        self.country = Country.objects.create(
            name='Испания',
            currency='Евро',
            vat_rate=21.0,
            language='Испанский'
        )
        self.category = PhraseCategory.objects.create(title='Приветствия')
    
    def test_create_phrase(self):
        """Тест создания фразы"""
        phrase = Phrase.objects.create(
            country=self.country,
            category=self.category,
            original_text='Hola',
            translated_text='Здравствуйте',
            transliteration='Ола'
        )
        self.assertEqual(phrase.original_text, 'Hola')
        self.assertEqual(phrase.translated_text, 'Здравствуйте')
        self.assertEqual(phrase.transliteration, 'Ола')
    
    def test_phrase_without_transliteration(self):
        """Тест создания фразы без транслитерации"""
        phrase = Phrase.objects.create(
            country=self.country,
            category=self.category,
            original_text='Gracias',
            translated_text='Спасибо'
        )
        self.assertEqual(phrase.transliteration, '')
    
    def test_phrase_str_method(self):
        """Тест строкового представления фразы"""
        phrase = Phrase.objects.create(
            country=self.country,
            category=self.category,
            original_text='Buenos días',
            translated_text='Доброе утро'
        )
        self.assertEqual(str(phrase), 'Buenos días')
    
    def test_phrase_country_relation(self):
        """Тест связи фразы со страной"""
        phrase = Phrase.objects.create(
            country=self.country,
            category=self.category,
            original_text='Adiós',
            translated_text='До свидания'
        )
        self.assertEqual(phrase.country.name, 'Испания')
    
    def test_phrase_category_relation(self):
        """Тест связи фразы с категорией"""
        phrase = Phrase.objects.create(
            country=self.country,
            category=self.category,
            original_text='Por favor',
            translated_text='Пожалуйста'
        )
        self.assertEqual(phrase.category.title, 'Приветствия')


class CountryModelTest(TestCase):
    """Тесты для модели Country"""
    
    def test_create_country(self):
        """Тест создания страны"""
        country = Country.objects.create(
            name='Россия',
            currency='Рубль',
            vat_rate=20.0,
            language='Русский'
        )
        self.assertEqual(country.name, 'Россия')
        self.assertEqual(country.currency, 'Рубль')
        self.assertEqual(country.vat_rate, 20.0)
        self.assertEqual(country.language, 'Русский')
    
    def test_country_str_method(self):
        """Тест строкового представления страны"""
        country = Country.objects.create(
            name='Япония',
            currency='Йена',
            vat_rate=10.0,
            language='Японский'
        )
        self.assertEqual(str(country), 'Япония')


class RelationsTest(TestCase):
    """Тесты связей между моделями"""
    
    def setUp(self):
        self.country = Country.objects.create(
            name='Великобритания',
            currency='Фунт',
            vat_rate=20.0,
            language='Английский'
        )
        self.category = PhraseCategory.objects.create(title='Категория')
    
    def test_country_articles_relation(self):
        """Тест: связь страна -> статьи"""
        article1 = Article.objects.create(country=self.country, title='Статья 1', link='link1')
        article2 = Article.objects.create(country=self.country, title='Статья 2', link='link2')
        
        articles = self.country.articles.all()
        self.assertEqual(articles.count(), 2)
    
    def test_country_apps_relation(self):
        """Тест: связь страна -> приложения"""
        app = LocalApp.objects.create(country=self.country, title='App', description='desc')
        
        apps = self.country.apps.all()
        self.assertEqual(apps.count(), 1)
        self.assertEqual(apps.first().title, 'App')
    
    def test_country_phrases_relation(self):
        """Тест: связь страна -> фразы"""
        phrase = Phrase.objects.create(
            country=self.country,
            category=self.category,
            original_text='Hello',
            translated_text='Привет'
        )
        
        phrases = self.country.phrase_set.all()
        self.assertEqual(phrases.count(), 1)
    
    def test_delete_country_cascades(self):
        """Тест: при удалении страны удаляются связанные статьи"""
        article = Article.objects.create(country=self.country, title='Статья', link='link')
        self.assertEqual(Article.objects.count(), 1)
        
        self.country.delete()
        self.assertEqual(Article.objects.count(), 0)
    
    def test_delete_category_sets_null(self):
        """Тест: при удалении категории поле category_id становится NULL"""
        phrase = Phrase.objects.create(
            country=self.country,
            category=self.category,
            original_text='Hello',
            translated_text='Привет'
        )
        
        self.category.delete()
        phrase.refresh_from_db()
        self.assertIsNone(phrase.category_id)