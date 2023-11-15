from typing import Any, Dict
import time
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from celery.result import AsyncResult
from celery import Celery

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
from pepper_app.forms import ScrapingRequest


def pre_action(request):
    return render(request, 'pre_action.html')


def action(request):
    category_type = "nowe"
    articles_to_retrieve = 120
    task = scrap_new_articles.apply_async()
    # output = ScrapPage(category_type, articles_to_retrieve)
    # output.get_items_details_depending_on_the_function()

    return HttpResponseRedirect(reverse("post_action"))


def post_action(request):
    items = PepperArticle.objects.all()

    return render(request, 'post_action.html', {'items': items})


def scrap_view(request):
    scraping_request_form = ScrapingRequest()

    context = {"scraping_request_form": ScrapingRequest()}

    if request.method == 'POST':
        scraping_request_form = ScrapingRequest(request.POST)
        if scraping_request_form.is_valid():
            category_type = scraping_request_form.cleaned_data["category_type"]
            articles_to_retrieve = scraping_request_form.cleaned_data["articles_to_retrieve"]
            start_page = scraping_request_form.cleaned_data["start_page"]

            task = scrap_new_articles.delay(category_type, articles_to_retrieve, start_page)
            request.session["task_id"] = task.id
            request.session["scrapping_in_progress"] = True

            context = {"scraping_request_form": ScrapingRequest(),
                       "task_id": request.session.get("task_id", False),
                       "result": request.session.get("result", False),
                       "scrapping_in_progress": request.session.get("scrapping_in_progress", False),
                       "scraping_finished": request.session.get("scraping_finished", False)
                       }

    return render(request, "scrap.html", context)


"""def scrap_status(request, task_id):
    # request.session["scraping_ready"] = False


    if request.method == 'GET':
        task = AsyncResult(task_id)

        if task.ready():
            context = {"task_id": request.session.get("task_id", False),
                       "result": task.get(),
                       "scrapping_in_progress": request.session.get("scrapping_in_progress", False),
                       "scraping_finished": request.session.get("scraping_finished", False),
                       }
            request.session["scrapping_in_progress"] = False
            request.session["scraping_finished"] = True
            request.session["result"] = task.get()

            
            return JsonResponse(context)

        else:
            return JsonResponse(context)"""

        
def scrap_status(request, task_id):
    # request.session["scraping_ready"] = False
    if request.method == 'GET':
        task = AsyncResult(task_id)
        if task.ready():
            request.session["scrapping_in_progress"] = False
            request.session["scraping_finished"] = True
            request.session["result"] = task.get()
     
            return redirect("scrap")
        
        else:
            return redirect("scrap")


"""def scrap_result(request, task_id):
    task = AsyncResult(task_id)
    request.session["result"] = task.get()

    return redirect("scrap.html")


def check_task_status(task_id):
    result = AsyncResult(task_id)

    if result.ready():
        return JsonResponse({'status': 'success', 'result': result.result})
    else:
        return JsonResponse({'status': 'pending'})"""


"""def scrap_view(request):

    context = {"scraping_request_form": ScrapingRequest()}
    scraping_request_form = ScrapingRequest(request.POST)

    if request.method == 'GET':
        task_id = request.session.get("task_id")
        request.session["scraping_in_progress"] = False

        if task_id:
            task = AsyncResult(task_id)
            request.session["scraping_in_progress"] = not task.ready()
        
        return render(request, 
                      "scrap.html", 
                      context,
                      request.session.get("scraping_in_progress", False))

    if request.method == 'POST':
        if scraping_request_form.is_valid():
            category_type = scraping_request_form.cleaned_data["category_type"]
            articles_to_retrieve = scraping_request_form.cleaned_data["articles_to_retrieve"]
            start_page = scraping_request_form.cleaned_data["start_page"]

            task = scrap_new_articles.delay(category_type, articles_to_retrieve, start_page)
            request.session["scraping_in_progress"] = True
            request.session["task_id"] = task.id


        redirect("scrap_status", task_id=str(task_id))"""

"""def scrap_status(request, task_id):

    task = AsyncResult(task_id)

    if task.ready():
        result = task.result
    
        context = {"scraping_request_form": ScrapingRequest(),
                    "result": result}

        return render(request, "scrap.html", context)

"""
