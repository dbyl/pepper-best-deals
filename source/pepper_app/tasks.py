from celery import shared_task
from celery import Celery
from django.core.cache import cache

from .scrap import ScrapPage
from pepper_app.models import (PepperArticle,
                                ScrapingStatistic,
                                UserRequest,
                                SuccessfulResponse)


app = Celery("configuration", include=['pepper_app.tasks'])


@app.task()
def scrap_new_articles(category_type, articles_to_retrieve, start_page):

    
    output = ScrapPage(category_type, articles_to_retrieve, start_page)
    all_items = output.get_items_details_depending_on_the_function()

    return all_items



@app.task()
def numbers(a, b, message=None):

    try:
        result = a + b
        if message:
            result = f"{message}: {result}"

        return result
    except Exception as ex:
        update_state(state=states.FAILURE, meta={'custom': '...'})
        raise Ignore()

