from requests.exceptions import ConnectionError, HTTPError, MissingSchema, ReadTimeout
import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from enum import Enum, IntEnum
from collections import Counter
import get_info
import csv



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
            time.sleep(0.05)
            item = list()
            item.append(get_info.GetItemId(article).get_data())
            item.append(get_info.GetItemName(article).get_data())
            item.append(get_info.GetItemDiscountPrice(article).get_data())
            item.append(get_info.GetItemPercentageDiscount(article).get_data())
            item.append(get_info.GetItemRegularPrice(article).get_data())
            item.append(get_info.GetItemAddedDate(article).get_data())
            item.append(get_info.GetItemUrl(article).get_data())
            all_items.append(item)

        return all_items

    def save_data_to_csv(self):

        header = ['item_id', 'name', 'discount_price', 'percentage_discount', 'regular_price', 'date_added', 'url']
        data = self.get_items_details()

        with open('scraped_data.csv', 'w', encoding='UTF8') as file:
            writer = csv.writer(file)

            writer.writerow(header)
            writer.writerows(data)



action_type = "/nowe?page="
start_page = 1
website_url = "https://www.pepper.pl"
articles_to_retrieve = 100

output = ScrapWebpage(website_url, action_type, articles_to_retrieve, start_page)
output.save_data_to_csv()