from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from pepper_app.models import (PepperArticle,
                                ScrapingStatistic,
                                UserRequest,
                                SuccessfulResponse)

from pepper_app.scrap import test_func

def main_page(request):

    return render(request, "base.html", {})

def test(request):
    test_func.delay()
    return HttpResponse("Done")