from typing import Any, Dict
from django.http import JsonResponse
from celery.result import AsyncResult
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.views.generic.list import ListView
from .tasks import scrap_new_articles
from pepper_app.forms import ScrapingRequest
from pepper_app.models import PepperArticle


class HomeView(ListView):

    model = PepperArticle
    context_object_name = "record"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        all_records = PepperArticle.objects.all().count()

        context = {
            "all_records": all_records,
        }

        return context

class GetNewArticles(TemplateView):

    def __init__(self, *args, **kwargs):
        self.template_name = "get_new_articles.html"

    def get(self, request):

        session_keys = ["get_new_articles_task_id",
                        "get_new_articles_result",
                        "get_new_articles_finished",
                        "get_new_articles_in_progress"
                        ]
        
        for key in session_keys:
            request.session[key] = False

        context = {key: request.session.get(key) for key in session_keys}
        context["get_new_articles_form"] = ScrapingRequest()

        return render(request, self.template_name, context)
    
    def post(self, request):
        get_new_articles_form = ScrapingRequest(request.POST)
        if get_new_articles_form.is_valid():
            category_type = get_new_articles_form.cleaned_data["category_type"]
            articles_to_retrieve = get_new_articles_form.cleaned_data["articles_to_retrieve"]

            get_new_articles_task = scrap_new_articles.delay(category_type, articles_to_retrieve)

            session_variables = {"get_new_articles_task_id": get_new_articles_task.id,
                                "get_new_articles_result": False,
                                "get_new_articles_finished": False,
                                "get_new_articles_in_progress": True,
                                "articles_to_retrieve": articles_to_retrieve,
                                }
            
            request.session.update(session_variables)

            context = {"get_new_articles_form": ScrapingRequest(),
                        "get_new_articles_task_id": request.session.get("get_new_articles_task_id"),
                        "get_new_articles_result": request.session.get("get_new_articles_result"),
                        "get_new_articles_in_progress": request.session.get("get_new_articles_in_progress"),
                        "get_new_articles_finished": request.session.get("get_new_articles_finished"),
                        }
            
            

        return render(request, self.template_name, context)


class CheckGetNewArticleTaskStatus(TemplateView):


    def get(self, request, **kwargs):
        get_new_articles_task_id = self.kwargs['get_new_articles_task_id']
        request.session["get_new_articles_result"] = False
        task = AsyncResult(get_new_articles_task_id)
        request.session["data"] = {}

        if task.ready():
            request.session["get_new_articles_in_progress"] = False
            request.session["get_new_articles_finished"] = True
            request.session["get_new_articles_result"] = True

            request.session["data"]["get_new_articles_in_progress"] = request.session["get_new_articles_in_progress"]
            request.session["data"]["get_new_articles_finished"] = request.session["get_new_articles_finished"]
            request.session["data"]["get_new_articles_result"] = request.session["get_new_articles_result"]
            
            return JsonResponse(request.session["data"], safe=False)
        
        else:
            request.session["get_new_articles_in_progress"] = True
            request.session["get_new_articles_result"] = False
            request.session["get_new_articles_finished"] = False

            request.session["data"]["get_new_articles_in_progress"] = request.session["get_new_articles_in_progress"]
            request.session["data"]["get_new_articles_finished"] = request.session["get_new_articles_finished"]
            request.session["data"]["get_new_articles_result"] = request.session["get_new_articles_result"]

            return JsonResponse(request.session["data"], safe=False)


def get_new_articles_task_result(request):

    results = PepperArticle.objects.order_by('-item_id')[:request.session.get("articles_to_retrieve")][::-1]
    context = {"results": results}
    
    return render(request, "get_new_articles_result.html", context)


def task_status(request):

    context = {"get_new_articles_task_id": request.session.get("get_new_articles_task_id"),
                "get_new_articles_result": request.session.get("get_new_articles_result"),
                "get_new_articles_in_progress": request.session.get("get_new_articles_in_progress"),
                "get_new_articles_finished": request.session.get("get_new_articles_finished"),
                }
    
    return JsonResponse(context)