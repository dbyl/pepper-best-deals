from django import forms


class ScrapingRequest(forms.Form):

    category_choices = (
                ("gorące","Gorące"),
                ("nowe", "Nowe"),
    )

    numbers_of_articles = (
        (5, 5),
        (10, 10),
        (15, 15),
        (20, 20),
        (30, 30),
        (40, 40),
        (50, 50),
        (100, 100),
    )

    category_type = forms.ChoiceField(
        required=True, choices=category_choices, initial="nowe"
    )

    articles_to_retrieve = forms.TypedChoiceField(
        required=True, choices=numbers_of_articles, coerce=int, initial=5
    )


class ScrapingSearchedArticleRequest(forms.Form):

    search_field = forms.CharField(required=True, coerce=str)
    avoid_expressions = forms.CharField(required=False, coerce=str)