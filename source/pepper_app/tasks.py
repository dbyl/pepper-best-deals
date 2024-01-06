from celery import Celery
from .scrape import ScrapePage
import time

app = Celery("configuration", include=['pepper_app.tasks'])

@app.task()
def scrape_new_articles(category_type, articles_to_retrieve):

    output = ScrapePage(category_type, articles_to_retrieve)
    output.get_items_details_depending_on_the_function()

@app.task()
def scrape_searched_articles(searched_article, articles_to_retrieve):

    category_type = "search"

    output1 = ScrapePage(category_type, articles_to_retrieve, searched_article=searched_article)
    output1.get_items_details_depending_on_the_function()

@app.task()
def scrape_all_new():

    category_type = "nowe"
    articles_to_retrieve = 9999999 

    output2 = ScrapePage(category_type, articles_to_retrieve)
    output2.get_items_details_depending_on_the_function()

@app.task()
def scrape_by_refreshing():

    scrape_continuously = True
    scrape_choosen_data = False
    category_type = "nowe"
    articles_to_retrieve = 9999999 

    output3 = ScrapePage(category_type, articles_to_retrieve, scrape_continuously=scrape_continuously, 
                         scrape_choosen_data=scrape_choosen_data)
    output3.get_items_details_depending_on_the_function()
