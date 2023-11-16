from django.contrib.auth import views as auth_views
from django.urls import path
from pepper_app import views
from pepper_app.views import (action, post_action, pre_action, scrap_view, scrap_status, session_check, scrap_result, check_task_status)

urlpatterns = [
    path('pre_action/', views.pre_action, name="pre_action"),
    path('action/', views.action, name="action"),
    path('post_action/', views.post_action, name="post_action"),
    path('scrap/', views.scrap_view, name="scrap"),
    path('scrap_status/<task_id>/', views.scrap_status, name="scrap_status"),
    path('scrap_result/<task_id>/', views.scrap_result, name="scrap_result"),
    path('session_check/', views.session_check, name="session_check"),
    path('check_task_status/<task_id>/', views.check_task_status, name='check_task_status'),
      ]
