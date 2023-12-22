from django.urls import path
from pepper_app import views
from pepper_app.views import (HomeView, GetNewArticles, CheckGetNewArticleTaskStatus, get_new_articles_task_result)

urlpatterns = [
    path('', HomeView.as_view(template_name="index.html"), name="home"),
    path('get_new_articles/', GetNewArticles.as_view(template_name="get_new_articles.html"), name="get_new_articles"),
    path('get_new_articles_check/<get_new_articles_task_id>/', CheckGetNewArticleTaskStatus.as_view(), name="get_new_articles_check"),
    path('get_new_articles_result/', views.get_new_articles_task_result, name="get_new_articles_result"),
    path('task_status/', views.task_status, name="task_status"),
    ]

