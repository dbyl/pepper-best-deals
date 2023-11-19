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


def scrap_view(request):
    scraping_request_form = ScrapingRequest()

    
    if request.method == 'POST':
        scraping_request_form = ScrapingRequest(request.POST)
        if scraping_request_form.is_valid():
            category_type = scraping_request_form.cleaned_data["category_type"]
            articles_to_retrieve = scraping_request_form.cleaned_data["articles_to_retrieve"]
            start_page = scraping_request_form.cleaned_data["start_page"]

            task = scrap_new_articles.delay(category_type, articles_to_retrieve, start_page)
            request.session["task_id"] = task.id
            request.session["scraping_in_progress"] = True


            context = {"scraping_request_form": ScrapingRequest(),
                       "task_id": request.session.get("task_id", False),
                       "result": request.session.get("result", False),
                       "scraping_in_progress": request.session.get("scraping_in_progress", False),
                       "scraping_finished": request.session.get("scraping_finished", False)
                       }
        return render(request, "scrap.html", context)

    
    if request.method == 'GET':
        context = {"scraping_request_form": ScrapingRequest(),
                        "task_id": request.session.get("task_id", False),
                        "result": request.session.get("result", False),
                        "scraping_in_progress": request.session.get("scraping_in_progress", False),
                        "scraping_finished": request.session.get("scraping_finished", False)
                        }

        return render(request, "scrap.html", context)


def session_check(request):

    context = {"task_id": request.session.get("task_id", False),
                "result": request.session.get("result", False),
                "scraping_in_progress": request.session.get("scraping_in_progress", False),
                "scraping_finished": request.session.get("scraping_finished", False)
                        }
    return JsonResponse(context)


def scrap_status(request, task_id):
    if request.method == 'GET':
        task = AsyncResult(task_id)
        if task.ready():
            request.session["scraping_in_progress"] = False
            request.session["scraping_finished"] = True
            request.session["result"] = task.get()
     
            return redirect("scrap")
        
        else:
            return redirect("scrap")
