from django.db import models
from django.contrib.auth.models import User

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
