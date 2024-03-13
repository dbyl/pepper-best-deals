from django import forms
from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"})
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.TextInput(attrs={"type": "password",
                                      "class": "form_widgets"}),
    )
    password2 = forms.CharField(
        label="Repeat password",
        widget=forms.TextInput(attrs={"type": "password",
                                      "class": "form_widgets"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginUserForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.TextInput(attrs={"type": "password",
                                      "class": "form_widgets"}),
    )


class PassResetForm(PasswordResetForm):

    email = forms.CharField(
        widget=forms.TextInput(attrs={"type": "charfield",
                                      "class": "form_widgets"})
    )


class PassSetForm(SetPasswordForm):

    new_password1 = forms.CharField(
        label="New password",
        widget=forms.TextInput(attrs={"type": "password",
                                      "class": "form_widgets"}),
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.TextInput(attrs={"type": "password",
                                      "class": "form_widgets"}),
    )


class PassChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label="Old password",
        widget=forms.TextInput(attrs={"type": "password",
                                      "class": "form_widgets"}),
    )
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.TextInput(attrs={"type": "password",
                                      "class": "form_widgets"}),
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.TextInput(attrs={"type": "password",
                                      "class": "form_widgets"}),
    )


class ScrapingRequest(forms.Form):


    numbers_of_articles = tuple((x, x) for x in range(10, 1001, 10))


    articles_to_retrieve = forms.TypedChoiceField(
        required=True, choices=numbers_of_articles, coerce=int, initial=10
    )


class ScrapingSearchedArticleRequest(forms.Form):

    numbers_of_articles = tuple((x, x) for x in range(10, 1001, 10))

    articles_to_retrieve = forms.TypedChoiceField(
        required=True, choices=numbers_of_articles, coerce=int, initial=10
    )
    scrape_data = forms.TypedChoiceField(required=True, choices=(("Yes", "Yes"), ("No", "No")), 
                                        coerce=str, initial="Yes", label="Scrape data: (If the data are already in the database you can skip scraping the data.)")
    
    searched_article = forms.CharField(required=True)
    excluded_terms = forms.CharField(required=False, label="Exclude terms: (item, item2, ... )")


class UserRequestForm(forms.Form):

    desired_article = forms.CharField(required=True)
    desired_price = forms.IntegerField(required=True)
    minimum_price = forms.IntegerField(required=False, initial=0)


class ArticlePriceHistoryForm(forms.Form):
    
    article = forms.CharField(required=True)
    price_min = forms.IntegerField(required=False)
    price_max = forms.IntegerField(required=False)
    excluded_terms = forms.CharField(required=False)
