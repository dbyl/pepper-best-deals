from django import forms


class ScrapingRequest(forms.Form):

    category_choices = (
                ("gorące","Gorące"),
                ("nowe", "Nowe"),
    )

    numbers_of_articles = tuple((x, x) for x in range(10, 401, 10))

    category_type = forms.ChoiceField(
        required=True, choices=category_choices, initial="nowe"
    )

    articles_to_retrieve = forms.TypedChoiceField(
        required=True, choices=numbers_of_articles, coerce=int, initial=5
    )


class ScrapingSearchedArticleRequest(forms.Form):

    numbers_of_articles = tuple((x, x) for x in range(10, 401, 10))

    articles_to_retrieve = forms.TypedChoiceField(
        required=True, choices=numbers_of_articles, coerce=int, initial=5
    )
    scrape_data = forms.TypedChoiceField(required=True, choices=(("Yes", "Yes"), ("No", "No")), 
                                        coerce=str, initial="Yes", label="Scrape data: (If the data are already in the database you can skip scraping the data.)")
    
    searched_article = forms.CharField(required=True)
    excluded_terms = forms.CharField(required=False, label="Exclude terms: (list terms: item, item2, ... )")