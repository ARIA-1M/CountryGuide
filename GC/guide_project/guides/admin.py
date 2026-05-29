from django.contrib import admin


from django.contrib import admin
from .models import Country, Article, LocalApp, PhraseCategory, Phrase

admin.site.register(Country)
admin.site.register(Article)
admin.site.register(LocalApp)
admin.site.register(PhraseCategory)
admin.site.register(Phrase)


# Register your models here.
