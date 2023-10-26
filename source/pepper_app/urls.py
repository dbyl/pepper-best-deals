from django.contrib.auth import views as auth_views
from django.urls import path
from pepper_app import views
from pepper_app.views import (calculate, action)

urlpatterns = [
    path("base/", views.calculate, name="calculate"),
    path('action/', views.action, name="action"),
]