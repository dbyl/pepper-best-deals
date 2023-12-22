from celery import Celery
from .scrap import ScrapPage

app = Celery("configuration", include=['pepper_app.tasks'])

@app.task()
def scrap_new_articles(category_type, articles_to_retrieve):

    output = ScrapPage(category_type, articles_to_retrieve)
    output.get_items_details_depending_on_the_function()

