from typing import Any, Dict
import time
from django.http import HttpResponse, JsonResponse
from celery.result import AsyncResult
from .tasks import add_numbers
from django.contrib import messages
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

from pepper_app.scrap import test_func

def calculate(request):
    a = 5
    b = 10
    time.sleep(5)
    result = add_numbers.delay(a, b)  # This starts the task asynchronously
    return render(request, 'base.html', {'task_id': result.id})


def action(request):
    if request.method == 'POST':
        from .scrap import ScrapPage

        category_type = "nowe"
        articles_to_retrieve = 120

        output = ScrapPage(category_type, articles_to_retrieve)
        output.get_items_details_depending_on_the_function()

        return HttpResponse("Button Clicked!")
    else:
        return render(request, 'action.html')


"""def test(request):
    test_func.delay()
    return HttpResponse("Done")"""