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
from django.views.decorators.http import require_POST



def task(request):
    scraping_request_form = ScrapingRequest(request.POST)

    if request.method == 'POST':
        if scraping_request_form.is_valid():
            category_type = scraping_request_form.cleaned_data["category_type"]
            articles_to_retrieve = scraping_request_form.cleaned_data["articles_to_retrieve"]

            task = scrap_new_articles.delay(category_type, articles_to_retrieve)

            request.session["task_id"] = task.id
            request.session["result"] = False
            request.session["scraping_finished"] = False
            request.session["scraping_in_progress"] = True
            
            context = {"scraping_request_form": ScrapingRequest(),
                        "task_id": request.session.get("task_id"),
                        "result": request.session.get("result"),
                        "scraping_in_progress": request.session.get("scraping_in_progress"),
                        "scraping_finished": request.session.get("scraping_finished"),
                        }
            
        return render(request, "task.html", context)

    if request.method == 'GET':

        request.session["task_id"] = False
        request.session["result"] = False
        request.session["scraping_finished"] = False
        request.session["scraping_in_progress"] = False

        context = {"scraping_request_form": ScrapingRequest(),
                    "task_id": request.session.get("task_id"),
                    "result": request.session.get("result"),
                    "scraping_in_progress": request.session.get("scraping_in_progress"),
                    "scraping_finished": request.session.get("scraping_finished"),
                    }

        return render(request, "task.html", context)
    

def task_check(request, task_id):

    if request.method == 'GET':
        request.session["result"] = False
        task = AsyncResult(task_id)
        if task.ready():
            request.session["scraping_in_progress"] = False
            request.session["scraping_finished"] = True
            request.session["result"] = True

            context = { "result": request.session.get("result"),
                        "scraping_in_progress": request.session.get("scraping_in_progress"),
                        "scraping_finished": request.session.get("scraping_finished"),
                        }
            
            return JsonResponse(context)
        
        else:
            request.session["scraping_in_progress"] = True
            request.session["result"] = False
            request.session["scraping_finished"] = False

            context = { "result": request.session.get("result"),
                        "scraping_in_progress": request.session.get("scraping_in_progress"),
                        "scraping_finished": request.session.get("scraping_finished"),
                        }
            
            return JsonResponse(context)
        

def task_status(request):


    context = {"task_id": request.session.get("task_id"),
                "result": request.session.get("result"),
                "scraping_in_progress": request.session.get("scraping_in_progress"),
                "scraping_finished": request.session.get("scraping_finished"),
                }
    
    return JsonResponse(context)


def task_result(request):
    
    context = {"result": request.session.get("result")}
    
    return render(request, "task_result.html", context)
        

def scrap_view(request):
    scraping_request_form = ScrapingRequest()

    if request.method == 'POST':
        scraping_request_form = ScrapingRequest(request.POST)
        if scraping_request_form.is_valid():
            category_type = scraping_request_form.cleaned_data["category_type"]
            articles_to_retrieve = scraping_request_form.cleaned_data["articles_to_retrieve"]
            task = scrap_new_articles.delay(category_type, articles_to_retrieve)
            
            request.session["result"] = False
            request.session["end_one_task"] = False    
            request.session["task_id"] = task.id
            request.session["scraping_in_progress"] = True


            context = {"scraping_request_form": ScrapingRequest(),
                        "task_id": request.session.get("task_id", task.id),
                        "result": request.session.get("result", False),
                        "scraping_in_progress": request.session.get("scraping_in_progress", True),
                        "scraping_finished": request.session.get("scraping_finished", False),
                        "end": request.session.get("end_one_task", False)
                        }
        return render(request, "scrap.html", context)

    
    if request.method == 'GET':

        context = {"scraping_request_form": ScrapingRequest(),
                       "task_id": request.session.get("task_id"),
                       "result": request.session.get("result", False),
                       "scraping_in_progress": request.session.get("scraping_in_progress", False),
                       "scraping_finished": request.session.get("scraping_finished", False),
                       "end": request.session.get("end_one_task", False)
                       }

        return render(request, "scrap.html", context)


def session_check(request):

    context = {"task_id": request.session.get("task_id"),
                "result": request.session.get("result"),
                "scraping_in_progress": request.session.get("scraping_in_progress"),
                "scraping_finished": request.session.get("scraping_finished"),
                "end": request.session.get("end_one_task")
                        }
    return JsonResponse(context)


def scrap_status(request, task_id):
    if request.method == 'GET':
        task = AsyncResult(task_id)
        if task.ready():
        
            request.session["scraping_in_progress"] = False
            request.session["scraping_finished"] = True
            request.session["result"] = task.get()
            request.session["end_one_task"] = True
            request.session["task_id"] = False
    
            
            context = {"task_id": request.session.get("task_id"),
                "result": request.session.get("result"),
                "scraping_in_progress": request.session.get("scraping_in_progress", False),
                "scraping_finished": request.session.get("scraping_finished", True),
                "end": request.session.get("end_one_task", True)}

            return JsonResponse(context)
        
        else:
            request.session["scraping_in_progress"] = True
            request.session["result"] = False
            request.session["scraping_finished"] = False
            request.session["end_one_task"] = False

            context = {"task_id": request.session.get("task_id"),
                "result": request.session.get("result", False),
                "scraping_in_progress": request.session.get("scraping_in_progress", True),
                "scraping_finished": request.session.get("scraping_finished", False),
                "end": request.session.get("end_one_task", False)}
            
            return JsonResponse(context)
