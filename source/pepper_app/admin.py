from django.contrib import admin

from .models import PepperArticles, ScrapingStatistics

admin.site.register(PepperArticles)
admin.site.register(ScrapingStatistics)