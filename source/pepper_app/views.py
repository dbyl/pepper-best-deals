from typing import Any, Dict
from django.http import JsonResponse
from celery.result import AsyncResult
from django.shortcuts import render
from .tasks import scrap_new_articles
from pepper_app.forms import ScrapingRequest


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
        request.session["data"] = {}

        if task.ready():
            request.session["scraping_in_progress"] = False
            request.session["scraping_finished"] = True
            request.session["result"] = task.get()

            request.session["data"]["scraping_in_progress"] = request.session["scraping_in_progress"]
            request.session["data"]["scraping_finished"] = request.session["scraping_finished"]
            request.session["data"]["result"] = request.session["result"]
            
            return JsonResponse(request.session["data"], safe=False)
        
        else:
            request.session["scraping_in_progress"] = True
            request.session["result"] = False
            request.session["scraping_finished"] = False

            request.session["data"]["scraping_in_progress"] = request.session["scraping_in_progress"]
            request.session["data"]["scraping_finished"] = request.session["scraping_finished"]
            request.session["data"]["result"] = request.session["result"]

            return JsonResponse(request.session["data"], safe=False)

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
        