from requests.exceptions import ConnectionError, HTTPError, MissingSchema, ReadTimeout
import logging
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta, date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from enum import Enum, IntEnum
from collections import Counter
import get_info



class ScrapWebpage:

    def __init__(self, website_url, action_type, articles_to_retrieve, start_page=1):
        self.website_url = website_url
        self.action_type = action_type
        self.articles_to_retrieve = articles_to_retrieve
        self.start_page = start_page

    def scrap_data(self):
        try:
            url_to_scrap = self.website_url + self.action_type + str(self.start_page)
            driver = webdriver.Chrome('./chromedriver')
            driver.set_window_size(1400,1000)
            driver.get(url_to_scrap)
            time.sleep(0.7)
            page = driver.page_source
            soup = BeautifulSoup(page, 'html.parser')
            return soup
        except ConnectionError as e:
            print(f"ConnectionError occured: {e}. \nTry again later")
        except MissingSchema as e:
            print(f"MissingSchema occured: {e}. \nMake sure that protocol indicator is icluded in the website url")
        except HTTPError as e:
            print(f"HTTPError occured: {e}. \nMake sure that website url is valid")
        except ReadTimeout as e:
            print(f"ReadTimeout occured: {e}. \nTry again later")

    def infinite_scroll_handling(self):
        try:
            flag = True
            retrived_articles = list()
            while flag:
                soup = self.scrap_data()
                articles = soup.find_all('article')
                retrived_articles += articles
                if len(retrived_articles) >= self.articles_to_retrieve:
                    flag = False
                    return retrived_articles[:self.articles_to_retrieve]
                self.start_page += 1
        except IndexError as e:
            raise IndexError("There aren't that many articles, try retrieve lower quantity of articles")



    def get_items_details(self):

        retrived_articles = self.infinite_scroll_handling()

        all_items = list()
        for article in retrived_articles:
            item = list()
            item.append(GetItemId(article).get_data())
            item.append(GetItemName(article).get_data())
            item.append(GetItemDiscountPrice(article).get_data())
            item.append(GetItemPercentageDiscount(article).get_data())
            item.append(GetItemRegularPrice(article).get_data())
            item.append(GetItemAddedDate(article).get_data())
            item.append(GetItemUrl(article).get_data())
            all_items.append(item)

        return all_items

"""    def dump_articles_to_txt(self):

        retrived_articles = self.infinite_scroll_handling()

        with open("scraped_data.txt", "w") as file:
            for item in retrived_articles:
                file.write(item)

    def read_articles_from_txt(self):

        articles = list()

        with open("scraped_data.txt", "r") as file:
            for item in file:
                article = item[:-1]
                articles.append(article)

        return articles"""


