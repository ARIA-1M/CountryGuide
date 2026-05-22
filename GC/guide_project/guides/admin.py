from django.contrib import admin

from django.contrib import admin
from .models import Country, Article, LocalApp

admin.site.register(Country)
admin.site.register(Article)
admin.site.register(LocalApp)

# Register your models here.
