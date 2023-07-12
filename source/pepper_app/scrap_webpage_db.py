from requests.exceptions import ConnectionError, HTTPError, MissingSchema, ReadTimeout
import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
from enum import Enum, IntEnum
from collections import Counter
import os
from pepper_app.get_info import GetItemAddedDate, GetItemDiscountPrice, GetItemId, GetItemName, GetItemPercentageDiscount, GetItemRegularPrice, GetItemUrl
import csv
import pandas as pd
import traceback
import sys
from typing import List, Union
import logging
import html5lib


from pepper_app.populate_database import LoadItemDetailesToDatabase, LoadDataFromCsv, LoadScrapingStatisticsToDatabase




class ScrapWebpage:

    def __init__(self, category_type: str, articles_to_retrieve: int, to_csv: bool = False,
                to_database: bool = False, to_statistics: bool = True, start_page: int = 1,
                searched_article: str = 'NA') -> None:
        self.category_type = category_type
        self.articles_to_retrieve = articles_to_retrieve
        self.to_database = to_database
        self.to_csv = to_csv
        self.to_statistics = to_statistics
        self.start_page = start_page
        self.searched_article = searched_article

    def scrap_data(self) -> str:

        try:
            if self.category_type == "nowe":
                url_to_scrap = "".join(["https://www.pepper.pl/", self.category_type, "?page=", str(self.start_page)])
            if self.category_type == "search":
                searched_article = str(self.searched_article.replace(" ","%20"))
                url_to_scrap = "".join(["https://www.pepper.pl/", self.category_type, "?q=",
                                        str(self.start_page), searched_article, "&page=", str(self.start_page)])
        except Exception as e:
            logging.warning(f"Invalid category type name, category must be 'nowe' or 'search':\
                            {e}\n Tracking: {traceback.format_exc()}")

        try:
            driver = webdriver.Chrome()
            driver.set_window_size(1400,1000)
            driver.get(url_to_scrap)
            time.sleep(0.7)
            page = driver.page_source
            soup = BeautifulSoup(page, "html5lib")
            return soup
        except ConnectionError as e:
            print(f"ConnectionError occured: {e}. \nTry again later")
        except MissingSchema as e:
            print(f"MissingSchema occured: {e}. \nMake sure that protocol indicator is icluded in the website url")
        except HTTPError as e:
            print(f"HTTPError occured: {e}. \nMake sure that website url is valid")
        except ReadTimeout as e:
            print(f"ReadTimeout occured: {e}. \nTry again later")


    def infinite_scroll_handling(self) -> List[str]:
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



    def get_items_details(self) -> None:

        start_time = datetime.now()

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

            if item not in all_items:
                all_items.append(item)
            else:
                continue

            if '' in item:
                logging.warning("Data retrieving failed. None values detected")
                break

            if to_csv == True:
                self.save_data_to_csv(item)

            if to_database == True:
                try:
                    LoadItemDetailesToDatabase(item).load_to_db()
                except Exception as e:
                    logging.warning(f"Populating PepperArticles table failed: {e}\n Tracking: {traceback.format_exc()}")

        end_time = datetime.now()
        action_execution_datetime = end_time - start_time

        if to_statistics == True:
            try:
                stats_info = self.get_scraping_stats_info(action_execution_datetime)
                LoadScrapingStatisticsToDatabase(stats_info).load_to_db()
            except Exception as e:
                logging.warning(f"Populating ScrapingStatistics table failed: {e}\n Tracking: {traceback.format_exc()}")


    def save_data_to_csv(self, item) -> None:

        columns = ['item_id', 'name', 'discount_price', 'percentage_discount',
                    'regular_price', 'date_added', 'url'] #to constans in the future

        header = False
        if not os.path.exists('scraped.csv'):
            header=True
            df = pd.DataFrame([item], columns=columns)
            df.to_csv('scraped.csv', header=header, index=False, mode='a')
        else:
            header = False
            df_e = pd.read_csv('scraped.csv')
            df = pd.DataFrame([item], columns=columns)
            if df['item_id'][0] not in df_e['item_id'].tolist():
                df.to_csv('scraped.csv', header=header, index=False, mode='a')


    def get_scraping_stats_info(self, action_execution_datetime) -> List[Union[str, int, bool, float]]:

        stats_info = list()

        category_type = self.category_type
        start_page = str(self.start_page)
        retrived_articles = str(self.articles_to_retrieve)
        time_of_the_action = datetime.now()
        action_execution_datetime = action_execution_datetime
        searched_article = self.searched_article
        to_csv = self.to_csv
        to_database  = self.to_database

        statistics_fields = [category_type, start_page, retrived_articles,
                            time_of_the_action, action_execution_datetime,
                            searched_article, to_csv, to_database]   #to constans in the future

        for field in statistics_fields:
            stats_info.append(field)

        return stats_info







category_type = "nowe"
start_page = 1
articles_to_retrieve = 10
to_csv = True
to_database = True
to_statistics = True
output = ScrapWebpage(category_type, articles_to_retrieve, to_csv, to_database, to_statistics, start_page)
output.get_items_details()