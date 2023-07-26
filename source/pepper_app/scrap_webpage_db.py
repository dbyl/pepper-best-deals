import sys
import csv
import os
import time
import logging
import html5lib
import pandas as pd
import traceback
from datetime import datetime, timedelta, date
from typing import List, Union
from bs4 import BeautifulSoup
from enum import Enum, IntEnum
from collections import Counter
from requests.exceptions import ConnectionError, HTTPError, MissingSchema, ReadTimeout
from django.utils.timezone import utc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pepper_app.get_info import (GetItemAddedDate,
                                GetItemDiscountPrice,
                                GetItemId,
                                GetItemName,
                                GetItemPercentageDiscount,
                                GetItemRegularPrice,
                                GetItemUrl)
from pepper_app.populate_database import (LoadItemDetailToDatabase,
                                        LoadDataFromCsv,
                                        LoadScrapingStatisticToDatabase)




class ScrapWebpage:


    def __init__(self, category_type: str, articles_to_retrieve: int, to_csv: bool=False,
                to_database: bool=False, to_statistics: bool=True, start_page: int=1,
                searched_article: str='NA', scrap_continuously: bool=False, scrap_choosen_data: bool=False) -> None:
        self.category_type = category_type
        self.articles_to_retrieve = articles_to_retrieve
        self.to_database = to_database
        self.to_csv = to_csv
        self.to_statistics = to_statistics
        self.start_page = start_page
        self.searched_article = searched_article
        self.scrap_continuously = scrap_continuously
        self.scrap_choosen_data = scrap_choosen_data

    def scrap_data(self) -> str:
        try:
            driver = webdriver.Chrome()
            driver.set_window_size(1400,1000)
            url_to_scrap = self.select_url()
            driver.get(url_to_scrap)
            time.sleep(0.7)
            page = driver.page_source
            soup = BeautifulSoup(page, "html5lib")
            return soup
        except ConnectionError as e:
            logging.warning(f"ConnectionError occured: {e}. \nTry again later")
        except MissingSchema as e:
            logging.warning(f"MissingSchema occured: {e}. \nMake sure that protocol indicator is icluded in the website url")
        except HTTPError as e:
            logging.warning(f"HTTPError occured: {e}. \nMake sure that website url is valid")
        except ReadTimeout as e:
            logging.warning(f"ReadTimeout occured: {e}. \nTry again later")

    def select_url(self) -> str:
        try:
            if self.scrap_continuously == True:
                url_to_scrap = "https://www.pepper.pl/nowe"
                return url_to_scrap
            elif self.category_type == "nowe":
                url_to_scrap = "".join(["https://www.pepper.pl/", self.category_type, "?page=", str(self.start_page)])
                return url_to_scrap
            elif self.category_type == "search":
                searched_article = str(self.searched_article.replace(" ","%20"))
                url_to_scrap = "".join(["https://www.pepper.pl/", self.category_type, "?q=",
                                        searched_article, "&page=", str(self.start_page)])
                return url_to_scrap
        except Exception as e:
            logging.warning(f"Invalid category type name, category must be 'nowe' or 'search':\
                            {e}\n Tracking: {traceback.format_exc()}")

    def infinite_scroll_handling(self) -> List[str]:
        try:
            flag = True
            retrived_articles = list()
            while flag:
                soup = self.scrap_data()
                flag = self.check_if_last_page(soup)
                if flag == False:
                    return retrived_articles[:self.articles_to_retrieve]

                flag = self.check_if_no_items_found(soup)
                if flag == False:
                    return retrived_articles[:self.articles_to_retrieve]
                if flag == True:
                    articles = soup.find_all('article')
                    retrived_articles += articles
                else:
                    return retrived_articles[:self.articles_to_retrieve]

                if len(retrived_articles) >= self.articles_to_retrieve:
                    flag = False
                    return retrived_articles[:self.articles_to_retrieve]
                self.start_page += 1
        except Exception as e:
            logging.warning(f"Infinite scroll failed:\
                            {e}\n Tracking: {traceback.format_exc()}")

    def get_items_details_depending_on_the_function(self) -> None:
        if self.scrap_continuously == True and self.scrap_choosen_data == False:
            flag = True
            while flag == True:
                retrived_articles = self.check_for_new_items_continuously()
                self.get_items_details(retrived_articles)
        elif self.scrap_continuously == False and self.scrap_choosen_data == True:
            retrived_articles = self.infinite_scroll_handling()
            self.get_items_details(retrived_articles)
        else:
            logging.warning(f"Matching get_items_details depending on the selected \
                            functionality failed: {e}\n Tracking: {traceback.format_exc()}")

    def get_items_details(self, retrived_articles) -> None:
        start_time = datetime.utcnow().replace(tzinfo=utc)
        all_items = list()
        try:
            for article in retrived_articles:
                item = list()
                item.append(GetItemId(article).get_data())
                item.append(GetItemName(article).get_data())
                item.append(GetItemDiscountPrice(article).get_data())
                item.append(GetItemPercentageDiscount(article).get_data())
                item.append(GetItemRegularPrice(article).get_data())
                item.append(GetItemAddedDate(article).get_data())
                item.append(GetItemUrl(article).get_data())
                if item not in all_items:
                    all_items.append(item)
                if '' in item:
                    logging.warning("Data retrieving failed. None values detected")
                    break
                if to_csv == True:
                    self.save_data_to_csv(item)
                if to_database == True:
                    try:
                        LoadItemDetailToDatabase(item).load_to_db()
                    except Exception as e:
                        logging.warning(f"Populating PepperArticles table failed: {e}\n Tracking: {traceback.format_exc()}")
        except Exception as e:
            logging.warning(f"Errr1:\
                        {e}\n Tracking: {traceback.format_exc()}")

        end_time = datetime.utcnow().replace(tzinfo=utc)
        action_execution_datetime = end_time - start_time

        if to_statistics == True:
            try:
                stats_info = self.get_scraping_stats_info(action_execution_datetime)
                LoadScrapingStatisticToDatabase(stats_info).load_to_db()
            except Exception as e:
                logging.warning(f"Populating ScrapingStatistics table failed: {e}\n Tracking: {traceback.format_exc()}")


    def save_data_to_csv(self, item) -> None:

        columns = ['item_id', 'name', 'discount_price', 'percentage_discount',
                    'regular_price', 'date_added', 'url'] #to constans in the future

        header = False
        if not os.path.exists('scraped.csv'):
            header = True
            df = pd.DataFrame([item], columns=columns)
            df.to_csv('scraped.csv', header=header, index=False, mode='a')
        else:
            header = False
            df_e = pd.read_csv('scraped.csv')
            df = pd.DataFrame([item], columns=columns)
            if df['item_id'][0] not in df_e['item_id'].tolist():
                df.to_csv('scraped.csv', header=header, index=False, mode='a')


    def get_scraping_stats_info(self, action_execution_datetime: datetime) -> List[Union[str, int, bool, float]]:

        stats_info = list()

        category_type = self.category_type
        start_page = str(self.start_page)
        retrived_articles_quantity = str(self.articles_to_retrieve)
        time_of_the_action = datetime.utcnow().replace(tzinfo=utc)
        action_execution_datetime = action_execution_datetime
        searched_article = self.searched_article
        to_csv = self.to_csv
        to_database  = self.to_database
        scrap_continuously = self.scrap_continuously
        scrap_choosen_data = self.scrap_choosen_data

        statistics_fields = [category_type, start_page, retrived_articles_quantity,
                            time_of_the_action, action_execution_datetime,
                            searched_article, to_csv, to_database, scrap_continuously, scrap_choosen_data]   #to constans in the future

        for field in statistics_fields:
            stats_info.append(field)

        return stats_info

    def check_if_last_page(self, soup: str) -> bool:

        """Checking 'nowe' category to verify if the scraped page is the last one."""

        try:
            searched_ending_string = soup.find_all('h1', {"class":"size--all-xl size--fromW3-xxl text--b space--b-2"})[0].get_text()
            if searched_ending_string.startswith("Ups"):
                logging.warning("No more pages to scrap.")
                return False
        except:
            return True


        """Checking 'search' category to verify if the scraped page is the last one."""

        try:
            searched_ending_string = soup.find_all('h3', {"class":"size--all-l"})[0].get_text()
            searched_articles_number = soup.find_all('span', {"class":"box--all-i size--all-s vAlign--all-m"})[0].get_text()
            searched_articles_number = int(searched_articles_number.replace(" ","").strip("\n\t Okazje()"))
            if searched_ending_string.startswith("Ups") and searched_articles_number > 0:
                logging.warning("No more pages to scrap.")
                return False
        except:
            return True

    def check_if_no_items_found(self, soup: str) -> bool:

        """Checking if searched item was found."""

        try:
            searched_ending_string = soup.find_all('h3', {"class":"size--all-l"})[0].get_text()
            searched_articles_number = soup.find_all('span', {"class":"box--all-i size--all-s vAlign--all-m"})[0].get_text()
            searched_articles_number = int(searched_articles_number.replace(" ","").strip("\n\t Okazje()"))
            if searched_ending_string.startswith("Ups") and searched_articles_number == 0:
                logging.warning("The searched item was not found.")
                return False
        except:
            return True

    def check_for_new_items_continuously(self) -> List[str]:

        retrived_articles = list()

        soup = self.scrap_data()
        time.sleep(20)
        articles = soup.find_all('article')
        retrived_articles += articles

        return retrived_articles






category_type = "nowe"
start_page = 2
searched_article = "fsdfsdfsdf"
articles_to_retrieve = 120
to_csv = True
to_database = True
to_statistics = True
scrap_continuously = False
scrap_choosen_data = True
output = ScrapWebpage(category_type, articles_to_retrieve, to_csv,
                        to_database, to_statistics, start_page, searched_article, scrap_continuously, scrap_choosen_data)

output.select_url()
output.get_items_details_depending_on_the_function()
