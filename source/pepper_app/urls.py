from django.urls import path
from pepper_app import views
from django.contrib.auth import views as auth_views

from pepper_app.forms import (PassChangeForm, 
                              PassResetForm, 
                              PassSetForm,
)
from pepper_app.views import (HomeView, 
                              GetNewArticles, 
                              CheckGetNewArticleTaskStatus, 
                              CheckGetNewArticleTaskResult,
                              GetSearchedArticles,
                              CheckGetSearchedArticleTaskStatus,
                              CheckGetSearchedArticleTaskResult,
                              ScrapeContinouslyTasks,
                              PriceAlertRequest,
                              ArticlePriceHistory,
                              )


urlpatterns = [
    path("register/", views.register_page, name="register"),
    path("login/", views.login_page, name="login"),
    path("login_required/", views.login_req, name="login_required"),
    path("logout/", views.logout_user, name="logout"),
    path("reset_password/",
        auth_views.PasswordResetView.as_view(
            form_class=PassResetForm, template_name="accounts/password_reset.html"
        ),name="reset_password",),
    path("change_password/",
        auth_views.PasswordChangeView.as_view(
            form_class=PassChangeForm,
            template_name="accounts/password_change_form.html",
        ),name="change_password",),
    path("change_password_complete/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/password_change_complete.html"
        ),name="password_change_done",),
    path("reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_sent.html"
        ),name="password_reset_done",),
    path("reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            form_class=PassSetForm, template_name="accounts/password_reset_form.html"
        ),name="password_reset_confirm",),
    path("reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_sent_complete.html"
        ),name="password_reset_complete",),
    path('', HomeView.as_view(template_name="index.html"), name="home"),
    path('get_new_articles/', GetNewArticles.as_view(template_name="get_new_articles.html"), name="get_new_articles"),
    path('get_new_articles_check/<get_new_articles_task_id>/', CheckGetNewArticleTaskStatus.as_view(), name="get_new_articles_check"),
    path('get_new_articles_result/', CheckGetNewArticleTaskResult.as_view(), name="get_new_articles_result"),
    path('get_searched_articles/', GetSearchedArticles.as_view(template_name="get_searched_articles.html"), name="get_searched_articles"),
    path('get_searched_articles_check/<get_searched_articles_task_id>/', CheckGetSearchedArticleTaskStatus.as_view(), name="get_searched_articles_check"),
    path('get_searched_articles_result/', CheckGetSearchedArticleTaskResult.as_view(), name="get_searched_articles_result"),
    path('task_status/', views.task_status, name="task_status"),
    path('scrape/', ScrapeContinouslyTasks.as_view(), name="scrape"),
    path('requests/', PriceAlertRequest.as_view(), name="requests"),
    path('price_history_chart/', ArticlePriceHistory.as_view(), name="price_history_chart"),
    ]



