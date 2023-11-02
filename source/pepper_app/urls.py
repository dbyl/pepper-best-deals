from django.contrib.auth import views as auth_views
from django.urls import path
from pepper_app import views
from pepper_app.views import (action, post_action, pre_action, task_result, run_task)

urlpatterns = [
    path('pre_action/', views.pre_action, name="pre_action"),
    path('action/', views.action, name="action"),
    path('post_action/', views.post_action, name="post_action"),

]