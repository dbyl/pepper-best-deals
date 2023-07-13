from django.contrib import admin

from .models import PepperArticle, ScrapingStatistic

admin.site.register(PepperArticle)
admin.site.register(ScrapingStatistic)