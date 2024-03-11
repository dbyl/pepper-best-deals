from typing import Any, Dict
from django.http import JsonResponse
from celery.result import AsyncResult
from celery import Celery
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from pepper_app.populate_database import LoadUserRequestToDatabase
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from .tasks import (scrape_new_articles,
                    scrape_searched_articles,
                    scrape_all_new,
                    scrape_by_refreshing,
                    )
from pepper_app.forms import (CreateUserForm,
                            LoginUserForm,
                            ScrapingRequest,
                            ScrapingSearchedArticleRequest,
                            UserRequestForm,
                            ArticlePriceHistoryForm,
                            )
from pepper_app.charts import article_price_history_chart
from pepper_app.models import PepperArticle
from django.db.models import Q
from django.shortcuts import redirect
import traceback
import logging
from decimal import Decimal








def register_page(request):

    register_form = CreateUserForm()

    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            register_form = CreateUserForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                user = register_form.cleaned_data.get("username")
                messages.success(request, "Account was created for " + user)
                return redirect("login")

    context = {"register_form": register_form}

    return render(request, "accounts/register.html", context)


def login_page(request):

    login_form = LoginUserForm()

    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            login_form = LoginUserForm(request.POST)
            username = request.POST.get("username")
            password = request.POST.get("password1")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.info(request, "Username or password is incorrect")

    context = {"login_form": login_form}

    return render(request, "accounts/login.html", context)


def login_req(request):
    login_form = LoginUserForm()

    if request.method == "POST":
        login_form = LoginUserForm(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password1")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/home/")
        else:
            messages.info(request, "Username or password is incorrect")

    context = {"login_form": login_form}

    return render(request, "accounts/login_required.html", context)


def logout_user(request):

    logout(request)

    return redirect("login")


class HomeView(ListView):
    """Creating home page"""
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
    """The class returns a view of the subpage and performs a celery task with the parameters set by the user."""
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
            articles_to_retrieve = get_new_articles_form.cleaned_data["articles_to_retrieve"]

            get_new_articles_task = scrape_new_articles.delay(articles_to_retrieve)

            session_variables = {"get_new_articles_task_id": get_new_articles_task.id,
                                "get_new_articles_result": False,
                                "get_new_articles_finished": False,
                                "get_new_articles_in_progress": True,
                                "articles_to_retrieve": articles_to_retrieve,
                                }
            
            request.session.update(session_variables)

            context = {"get_new_articles_form": ScrapingRequest(initial={'articles_to_retrieve':articles_to_retrieve}),
                        "get_new_articles_task_id": request.session.get("get_new_articles_task_id"),
                        "get_new_articles_result": request.session.get("get_new_articles_result"),
                        "get_new_articles_in_progress": request.session.get("get_new_articles_in_progress"),
                        "get_new_articles_finished": request.session.get("get_new_articles_finished"),
                        }

        return render(request, self.template_name, context)


class CheckGetNewArticleTaskStatus(TemplateView):
    """The class checks if the celery task is ready by returning the corresponding django session values.""" 
    def get(self, request, **kwargs):
        get_new_articles_task_id = self.kwargs['get_new_articles_task_id']
        request.session["get_new_articles_result"] = False
        task = AsyncResult(get_new_articles_task_id)
        request.session["data"] = dict()

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


class CheckGetNewArticleTaskResult(TemplateView):
    """The class returns results on a database query for new articles.""" 
    def __init__(self):
        self.template_name = "get_new_articles_result.html"

    def get(self, request):
        results = PepperArticle.objects.order_by('-date_added').order_by('-item_id')[:request.session.get("articles_to_retrieve")][::-1]
        context = {"results": results}

        return render(request, self.template_name, context)


class GetSearchedArticles(TemplateView):
    """The class returns a view of the subpage and performs a celery task with the parameters set by the user (searching articles)."""
    def __init__(self, *args, **kwargs):
        self.template_name = "get_searched_articles.html"

    def get(self, request):
        session_keys = ["get_searched_articles_task_id",
                        "get_searched_articles_result",
                        "get_searched_articles_finished",
                        "get_searched_articles_in_progress",
                        ]
        
        for key in session_keys:
            request.session[key] = False

        context = {key: request.session.get(key) for key in session_keys}
        context["get_searched_articles_form"] = ScrapingSearchedArticleRequest()

        return render(request, self.template_name, context)
    
    def post(self, request):
        get_searched_articles_form = ScrapingSearchedArticleRequest(request.POST)
        if get_searched_articles_form.is_valid():
            articles_to_retrieve = get_searched_articles_form.cleaned_data["articles_to_retrieve"]
            searched_article = get_searched_articles_form.cleaned_data["searched_article"]
            scrape_data = get_searched_articles_form.cleaned_data["scrape_data"]
            excluded_terms = get_searched_articles_form.cleaned_data["excluded_terms"]

            if scrape_data == "Yes":
                get_searched_articles_task = scrape_searched_articles.delay(searched_article, articles_to_retrieve)

                
                session_variables = {"get_searched_articles_task_id": get_searched_articles_task.id,
                                    "get_searched_articles_in_progress": True,
                                    "searched_articles_to_retrieve": articles_to_retrieve,
                                    "searched_article": searched_article,
                                    "scrape_data": scrape_data,
                                    "excluded_terms": excluded_terms,
                                    }             

                request.session.update(session_variables)
                
            else:
                session_variables = {"searched_articles_to_retrieve": articles_to_retrieve,
                                    "searched_article": searched_article,
                                    "scrape_data": scrape_data,
                                    "excluded_terms": excluded_terms,}
                
                request.session.update(session_variables)

                return redirect('get_searched_articles_result')

            context = {"get_searched_articles_form": ScrapingSearchedArticleRequest(initial={'articles_to_retrieve':articles_to_retrieve,
                                                                                            'searched_article':searched_article,
                                                                                            'scrape_data':scrape_data,
                                                                                            'excluded_terms': excluded_terms}),
                        "get_searched_articles_task_id": request.session.get("get_searched_articles_task_id"),
                        "get_searched_articles_result": request.session.get("get_searched_articles_result"),
                        "get_searched_articles_in_progress": request.session.get("get_searched_articles_in_progress"),
                        "get_searched_articles_finished": request.session.get("get_searched_articles_finished"),
                        "searched_article": request.session.get("searched_article"),
                        "scrape_data": request.session.get("scrape_data"),
                        "excluded_terms": request.session.get("excluded_terms"),
                        }

        return render(request, self.template_name, context)


class CheckGetSearchedArticleTaskStatus(TemplateView):
    """The class checks if the celery task is ready by returning the corresponding django session values.""" 
    def get(self, request, **kwargs):
        get_searched_articles_task_id = self.kwargs['get_searched_articles_task_id']
        request.session["get_searched_articles_result"] = False
        task = AsyncResult(get_searched_articles_task_id)
        request.session["searching_task_data"] = dict()

        if task.ready():
            request.session["get_searched_articles_in_progress"] = False
            request.session["get_searched_articles_finished"] = True
            request.session["get_searched_articles_result"] = True

            request.session["searching_task_data"]["get_searched_articles_in_progress"] = request.session["get_searched_articles_in_progress"]
            request.session["searching_task_data"]["get_searched_articles_finished"] = request.session["get_searched_articles_finished"]
            request.session["searching_task_data"]["get_searched_articles_result"] = request.session["get_searched_articles_result"]
            
            return JsonResponse(request.session["searching_task_data"], safe=False)
        else:
            request.session["get_searched_articles_in_progress"] = True
            request.session["get_searched_articles_result"] = False
            request.session["get_searched_articles_finished"] = False

            request.session["searching_task_data"]["get_searched_articles_in_progress"] = request.session["get_searched_articles_in_progress"]
            request.session["searching_task_data"]["get_searched_articles_finished"] = request.session["get_searched_articles_finished"]
            request.session["searching_task_data"]["get_searched_articles_result"] = request.session["get_searched_articles_result"]

            return JsonResponse(request.session["searching_task_data"], safe=False)


class CheckGetSearchedArticleTaskResult(TemplateView):
    """The class returns results on a database query for new articles.""" 
    def __init__(self):
        self.template_name = "get_searched_articles_result.html"

    def searching_conditions(self, request):
        """Adding conditions for better data filtering. 
        Necessary to improve the search by name and to include expressions to be ignored."""
        conditions = Q()

        searched_article_list = request.session.get('searched_article').split()
        excluded_terms = request.session.get('excluded_terms')

        if len(excluded_terms) != 0:
            excluded_terms_list = excluded_terms.split(', ')
            for term in excluded_terms_list:
                conditions &= ~Q(article_name__icontains=term)
        
        for word in searched_article_list:
            conditions &= Q(article_name__icontains=word)
        
        return conditions


    def get(self, request):
        conditions = self.searching_conditions(request)  
        results = PepperArticle.objects.filter(conditions).order_by('date_added')[:request.session.get("searched_articles_to_retrieve")][::-1]

        session_variables = {"searched_articles_to_retrieve": False,
                            "searched_article": False,
                            "scrape_data": False,
                            "excluded_terms": False,}  
        request.session.update(session_variables)

        context = {"results": results}

        return render(request, self.template_name, context)


class ScrapeContinouslyTasks(TemplateView):
    """The view class contains implementations of the continuous page scraping function in two variants."""
    def __init__(self):
        self.template_name = "scrape.html"
    
    def get(self, request):

        context = {"scrape_all_new_task_in_progress": request.session.get("scrape_all_new_task_in_progress"),
                    "scrape_all_new_invalid_action": request.session.get("scrape_all_new_invalid_action"),
                    "scrape_by_refreshing_task_in_progress": request.session.get("scrape_by_refreshing_task_in_progress"),
                    }
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        scrape_all_new_task_status = request.POST.get("scrape_all_new_task_status")
        scrape_by_refreshing_task_status = request.POST.get("scrape_by_refreshing_task_status")
        
        if scrape_all_new_task_status == 'start':
            if request.session.get("scrape_all_new_task_in_progress") == True:
                session_variables = {"scrape_all_new_invalid_action": True}
                pass
            else:
                scrape_all_new_task = scrape_all_new.delay()

                session_variables = {"scrape_all_new_task_id": scrape_all_new_task.id,
                                    "scrape_all_new_task_in_progress": True,
                                    "scrape_all_new_invalid_action": False}
        if scrape_all_new_task_status == 'stop':
            scrape_all_new_task_id = request.session.get("scrape_all_new_task_id")
            if scrape_all_new_task_id == False:
                pass
            else:
                task = AsyncResult(request.session.get("scrape_all_new_task_id"))
                task.revoke(terminate=True)

            session_variables = {"scrape_all_new_task_in_progress": False,
                                "scrape_all_new_task_id": False,
                                "scrape_all_new_invalid_action": False}
        
        
        if scrape_by_refreshing_task_status == 'start':
            if request.session.get("scrape_by_refreshing_task_in_progress") == True:
                session_variables = {"scrape_by_refreshing_invalid_action": True}
                pass
            else:
                scrape_by_refreshing_task = scrape_by_refreshing.delay()

                session_variables = {"scrape_by_refreshing_task_id": scrape_by_refreshing_task.id,
                                    "scrape_by_refreshing_task_in_progress": True,
                                    "scrape_by_refreshing_invalid_action": False,}
        if scrape_by_refreshing_task_status == 'stop':
            scrape_by_refreshing_task_id = request.session.get("scrape_by_refreshing_task_id")
            if scrape_by_refreshing_task_id == False:
                pass
            else:
                task1 = AsyncResult(request.session.get("scrape_by_refreshing_task_id"))
                task1.revoke(terminate=True)

            session_variables = {"scrape_by_refreshing_task_in_progress": False,
                                "scrape_by_refreshing_task_id": False,
                                "scrape_by_refreshing_invalid_action": False}


        request.session.update(session_variables)

        context = {"scrape_all_new_task_in_progress": request.session.get("scrape_all_new_task_in_progress"),
                   "scrape_by_refreshing_task_in_progress": request.session.get("scrape_by_refreshing_task_in_progress")
                   }

        return render(request, self.template_name, context)


class PriceAlertRequest(TemplateView):
    """The class contains functions that allow users to make
      their own notification requests if an item reaches the desired price."""
    def __init__(self):
        self.template_name = "requests.html"

    @method_decorator(login_required, name='login_required')
    def get(self, request):

        context = {"user_request_form": UserRequestForm()}

        return render(request, self.template_name, context)
    
    @method_decorator(login_required, name='login_required')
    def post(self, request):

        user_request_form = UserRequestForm(request.POST)
        if user_request_form.is_valid():

            desired_article = user_request_form.cleaned_data["desired_article"]
            desired_price = user_request_form.cleaned_data["desired_price"]
            minimum_price = user_request_form.cleaned_data["minimum_price"]
            request_time = timezone.now()
            user_id = request.user


            item = [desired_article, desired_price, minimum_price, request_time, user_id]
            try:    
                LoadUserRequestToDatabase(item).load_to_db()
            except Exception as e:
                logging.warning(f"Saving data to csv failed: {e}\n Tracking: {traceback.format_exc()}")


            context = {"user_request_form": UserRequestForm(initial={'desired_article':desired_article,
                                                                        'desired_price':desired_price,
                                                                        'minimum_price':minimum_price})}
        return render(request, self.template_name, context)


class ArticlePriceHistory(TemplateView):
    """The class contains functions that allow users to generate a 
    chart of the history of price changes of a given item for the set parameters."""
    def __init__(self):
        self.template_name = "price_history_chart.html"

    def searching_conditions(self, article, price_min, price_max, excluded_terms):
        """Function returns filter conditions for user-set parameters"""
        conditions = Q()

        article_list = article.split()
                
        for word in article_list:
            conditions &= Q(article_name__icontains=word)        
        
        if excluded_terms:
            excluded_terms_list = excluded_terms.split(', ')
            for term in excluded_terms_list:
                conditions &= ~Q(article_name__icontains=term)

        if price_min:
            conditions &= Q(discount_price__gte=price_min)

        if price_max:
            conditions &= Q(discount_price__lte=price_max)
        
        return conditions
    

    def generate_article_price_history_chart(self, filtered_data, article):
        """The function that generates the html-chart."""

        discount_price_list = list(filtered_data.values_list("discount_price", flat=True))
        date_added_list = list(filtered_data.values_list("date_added", flat=True))
        article_name_list = list(filtered_data.values_list("article_name", flat=True))
        
        chart_html = article_price_history_chart(discount_price_list, date_added_list, article_name_list, article).to_html()
       
        return chart_html
    

    @method_decorator(login_required, name='login_required')
    def get(self, request):

        article = self.request.GET.get("article")
        price_min = self.request.GET.get("price_min")
        price_max = self.request.GET.get("price_max")
        excluded_terms = self.request.GET.get("excluded_terms")

        context = {"article_price_history_form": ArticlePriceHistoryForm()}

        article_price_history_form = ArticlePriceHistoryForm(self.request.GET)

        if article_price_history_form.is_valid():
            excluded_terms = self.request.GET.get("excluded_terms")
            conditions = self.searching_conditions(article, price_min, price_max, excluded_terms)  
            filtered_data = PepperArticle.objects.filter(conditions).values("discount_price", "date_added", "article_name")

            chart_html = self.generate_article_price_history_chart(filtered_data, article)


            context = {"chart_html": chart_html,
                       "excluded_terms": excluded_terms,
                        "article_price_history_form": ArticlePriceHistoryForm(initial={'article':article,
                                                                        'price_min':price_min,
                                                                        'price_max':price_max,
                                                                        'excluded_terms':excluded_terms})}

        return render(request, self.template_name, context)
    




    
