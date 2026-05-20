from django.db import models
from django.contrib.auth.models import User

# Модель страны
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

# Модель поездки
class Trip(models.Model):
    сountry = models.ForeignKey(Country,on_delete=models.CASCADE, related_name='сountry',verbose_name="Страна")
    user = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name="Пользователь")
    start_date = models.DateField(verbose_name="Дата начала поездки")
    end_date = models.DateField(verbose_name="Дата окончания поездки")
   
    def __str__(self):
            return f"{self.сountry.name} - {self.start_date}"  
    class Meta:
           verbose_name = "Поездка"
           verbose_name_plural = "Поездки"


# Модель бюджета
class Budget(models.Model):
    trip = models.ForeignKey(Trip,on_delete=models.CASCADE, related_name='trip',verbose_name="Поездка")
    amount = models.DecimalField(max_digits=3,decimal_places=2,verbose_name="Бюджет")
    daily_limit = models.DecimalField(max_digits=3,decimal_places=2,verbose_name="Лимит на день")
    threshold_limit = models.BooleanField(verbose_name="Наличие пороговых уведомлений")    
    spent = models.DecimalField(max_digits=3,decimal_places=2,verbose_name="Расход")
   
    def __str__(self):
            return self.amount   
    class Meta:
           verbose_name = "Бюджет"
           verbose_name_plural = "Бюджеты"