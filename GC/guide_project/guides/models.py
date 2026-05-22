from django.db import models

# Модель для стран
class Country(models.Model):
    name = models.CharField(max_length=100,verbose_name="Название страны")
    currency = models.CharField(max_length=100,verbose_name="Название ваоюты")
    vat_rate = models.DecimalField(max_digits=3,decimal_places=2,verbose_name="Налог (%)")
    language = models.CharField(max_length=100,verbose_name="Язык")
   
    def __str__(self):
            return self.name 
    class Meta:
           verbose_name = "Страна"
           verbose_name_plural = "Страны"


class Article(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    link = models.URLField(verbose_name="Ссылка на статью")
    update = models.DateField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

from django.db import models

class LocalApp(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='apps')
    title = models.CharField(max_length=200, verbose_name="Название приложения")
    description = models.TextField(verbose_name="Описание")
    logo = models.ImageField(upload_to='apps_logos/', blank=True, null=True, verbose_name="Логотип")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Приложение"
        verbose_name_plural = "Приложения"