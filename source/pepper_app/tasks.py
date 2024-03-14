import time

from celery import Celery

from .scrape import ScrapePage

app = Celery("configuration", include=["pepper_app.tasks"])


@app.task()
def scrape_new_articles(articles_to_retrieve):
    category_type = "nowe"

    s = ScrapePage(category_type, articles_to_retrieve)
    s.get_items_details_depending_on_the_function()


@app.task()
def scrape_searched_articles(searched_article, articles_to_retrieve):
    category_type = "search"

    s = ScrapePage(
        category_type, articles_to_retrieve, searched_article=searched_article
    )
    s.get_items_details_depending_on_the_function()


@app.task()
def scrape_all_new():
    category_type = "nowe"
    articles_to_retrieve = 9999999

    s = ScrapePage(category_type, articles_to_retrieve)
    s.get_items_details_depending_on_the_function()


@app.task()
def scrape_by_refreshing():
    scrape_continuously = True
    scrape_choosen_data = False
    category_type = "nowe"
    articles_to_retrieve = 9999999

    s = ScrapePage(
        category_type,
        articles_to_retrieve,
        scrape_continuously=True,
        scrape_choosen_data=False,
    )
    s.get_items_details_depending_on_the_function()
