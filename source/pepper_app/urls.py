from django.contrib.auth import views as auth_views
from django.urls import path
from pepper_app import views
from pepper_app.views import (action, post_action, pre_action, post_celery)

urlpatterns = [
    path('action/', views.action, name="action"),
    path('post_action/', views.post_action, name="post_action"),
    path('pre_action/', views.pre_action, name="pre_action"),
    #path('pre_celery/', views.pre_celery, name="pre_celery"),
    path('celery_scrapping/', views.celery_scrapping, name='celery_scrapping'),
    path('post_celery/<str:task_id>/', views.post_celery, name='post_celery'),
]