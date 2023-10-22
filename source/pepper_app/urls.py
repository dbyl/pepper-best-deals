from django.contrib.auth import views as auth_views
from django.urls import path
from pepper_app import views
from pepper_app.views import (main_page)

urlpatterns = [
    path("base/", views.main_page, name="main page"),
    path("", views.test, name="test"),
]