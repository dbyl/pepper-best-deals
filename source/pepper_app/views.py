from typing import Any, Dict
import time
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from celery.result import AsyncResult
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from .scrap import ScrapPage
from pepper_app.models import (PepperArticle,
                                ScrapingStatistic,
                                UserRequest,
                                SuccessfulResponse)



def pre_action(request):

    return render(request, 'pre_action.html')

def action(request):

    category_type = "nowe"
    articles_to_retrieve = 120

    output = ScrapPage(category_type, articles_to_retrieve)
    output.get_items_details_depending_on_the_function()

    return HttpResponseRedirect(reverse("post_action"))


def post_action(request):

    items = PepperArticle.objects.all()

    return render(request, 'post_action.html', {'items': items})
