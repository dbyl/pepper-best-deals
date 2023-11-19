from django.contrib.auth import views as auth_views
from django.urls import path
from pepper_app import views
from pepper_app.views import (scrap_view, scrap_status, session_check)

urlpatterns = [
    path('scrap/', views.scrap_view, name="scrap"),
    path('scrap_status/<task_id>/', views.scrap_status, name="scrap_status"),
    path('session_check/', views.session_check, name="session_check"),
      ]
