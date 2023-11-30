from django.contrib.auth import views as auth_views
from django.urls import path
from pepper_app import views
from pepper_app.views import (task, task_check, task_result)

urlpatterns = [
    path('task/', views.task, name="task"),
    path('task_check/<task_id>/', views.task_check, name="task_check"),
    path('task_status/', views.task_status, name="task_status"),
    path('task_result/', views.task_result, name="task_result"),
      ]
