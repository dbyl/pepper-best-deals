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
from .tasks import scrap_new_articles
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

"""def celery_scrapping(request):
    if request.method == 'POST':

        result = scrap_new_articles.delay()  # Trigger the Celery task

        return render(request, 'post_celery.html', {'task_id': result.task_id, 'result':result.result})
    return render(request, 'pre_celery.html')"""

def pre_celery(request):
    return render(request, 'pre_celery.html')


def celery_scrapping(request):
    #if request.method == 'POST':
    result = scrap_new_articles.delay()  # Trigger the Celery task
    context = {'task_id': result.id}

    return redirect("post_celery", context)
    #return HttpResponseRedirect(reverse("post_celery", context))

    #return render(request, 'post_celery.html', {'task_id': result.result})
    #return render(request, 'pre_celery.html')

def post_celery(request, task_id):
    result = AsyncResult(task_id)

    return JsonResponse({'status': 'SUCCESS', 'result': result.result})

    if result.ready():
        return JsonResponse({'status': 'SUCCESS', 'result': result.result})
    elif result.failed():
        return JsonResponse({'status': 'FAILURE', 'message': 'Task failed'})
    else:
        return JsonResponse({'status': 'PENDING'})


def post_celery2(request, task_id):

    result = PepperArticle.objects.all()

    return render(request, 'post_celery.html', {'result': result})