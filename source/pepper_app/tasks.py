from celery import shared_task
from .scrap import ScrapPage
from pepper_app.models import (PepperArticle,
                                ScrapingStatistic,
                                UserRequest,
                                SuccessfulResponse)

@shared_task
def scrap_new_articles():
    category_type = "nowe"
    articles_to_retrieve = 100

    output = ScrapPage(category_type, articles_to_retrieve)
    output.get_items_details_depending_on_the_function()
   # articles = PepperArticle.objects.all()

   # result = [{'title': article.title, 'content': article.content, 'date': article.date} for article in articles]

   # return result


