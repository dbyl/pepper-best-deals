from django.contrib import admin

from .models import PepperArticle, ScrapingStatistic, UserRequest, SuccessfulResponse

admin.site.register(PepperArticle)
admin.site.register(ScrapingStatistic)
admin.site.register(UserRequest)
admin.site.register(SuccessfulResponse)
