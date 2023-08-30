import sys
import csv
import os
import time
import logging
import html5lib
import pandas as pd
import signal
import traceback
from datetime import datetime, timedelta, date, timezone
from typing import List, Union
from bs4 import BeautifulSoup
from enum import Enum, IntEnum
from collections import Counter
from requests.exceptions import ConnectionError, HTTPError, MissingSchema, ReadTimeout
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from pepper_app.get_info import (GetItemAddedDate,
                                GetItemDiscountPrice,
                                GetItemId,
                                GetItemName,
                                GetItemPercentageDiscount,
                                GetItemRegularPrice,
                                GetItemUrl)
from pepper_app.populate_database import (LoadItemDetailsToDatabase,
                                        LoadDataFromCsv,
                                        LoadScrapingStatisticsToDatabase)
from pepper_app.environment_config import CustomEnvironment
from pepper_app.constans import (CSV_COLUMNS,
                                STATS_HEADER)




class ScrapPage:


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

    def scrap_page(self, url_to_scrap: str, driver: WebDriver=None) -> BeautifulSoup:
        """Setting up selenium webdriver, scraping page with bs4."""
        try:
            if driver is None:
                driver = webdriver.Chrome()
            driver.set_window_size(1400,1000)
            driver.get(url_to_scrap)
            time.sleep(0.7)
            page = driver.page_source
            soup = BeautifulSoup(page, "html5lib")
            return soup
        except ConnectionError as e:
            raise ConnectionError(f"ConnectionError occured: {e}. \nTry again later")
        except MissingSchema as e:
            raise MissingSchema(f"MissingSchema occured: {e}. \nMake sure that protocol indicator is icluded in the website url")
        except HTTPError as e:
            raise HTTPError(f"HTTPError occured: {e}. \nMake sure that website url is valid")
        except ReadTimeout as e:
            raise ReadTimeout(f"ReadTimeout occured: {e}. \nTry again later")

    def select_url(self) -> str:
        """Selection of the website address depending on the type of scrapping."""
        if self.scrap_continuously == True:
            url_to_scrap = "".join([CustomEnvironment.get_url(), "nowe"])
            return url_to_scrap
        elif self.category_type == "nowe" and self.scrap_continuously == False:
            url_to_scrap = "".join([CustomEnvironment.get_url(), self.category_type, "?page=", str(self.start_page)])
            return url_to_scrap
        elif self.category_type == "search" and self.scrap_continuously == False:
            searched_article = str(self.searched_article.replace(" ","%20"))
            url_to_scrap = "".join([CustomEnvironment.get_url(), self.category_type, "?q=",
                                    searched_article, "&page=", str(self.start_page)])
            return url_to_scrap
        else:
            raise Exception(f"The variables were defined incorrectly.")


    def infinite_scroll_handling(self) -> List[str]:
        """Handling scraping through subsequent pages."""
        try:
            flag = True
            retrived_articles = list()
            while flag:
                url_to_scrap = self.select_url()
                soup = self.scrap_page(url_to_scrap)
                flag_nowe = CheckConditions(soup).check_if_last_page_nowe()
                flag_search = CheckConditions(soup).check_if_last_page_search()
                if flag_nowe == False or flag_search == False:
                    flag = False
                    return retrived_articles[:self.articles_to_retrieve]
                flag = CheckConditions(soup).check_if_no_items_found()
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
            raise Exception(f"Infinite scroll failed:\
                            {e}\n Tracking: {traceback.format_exc()}")



    def get_items_details_depending_on_the_function(self) -> None:
        """Completing the list of articles and extracting data details depending on the type of scrapping."""
        if self.scrap_continuously == True and self.scrap_choosen_data == False:
            while True:
                retrived_articles = self.scrap_continuously_by_refreshing_page()
                self.get_items_details(retrived_articles)
        elif self.scrap_continuously == False and self.scrap_choosen_data == True:
            retrived_articles = self.infinite_scroll_handling()
            self.get_items_details(retrived_articles)
        else:
            raise Exception(f"Matching get_items_details depending on the selected \
                            functionality failed. \n Tracking: {traceback.format_exc()}")


    def get_items_details(self, retrived_articles) -> list():
        """Getting item detailes."""
        start_time = datetime.utcnow().replace(tzinfo=timezone.utc)
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
                if self.to_csv:
                    self.save_data_to_csv(item)
                if self.to_database:
                    LoadItemDetailsToDatabase(item).load_to_db()
            return all_items
        except Exception as e:
            logging.warning(f"Getting item details failed :\
                        {e}\n Tracking: {traceback.format_exc()}")

        end_time = datetime.utcnow().replace(tzinfo=timezone.utc)
        action_execution_datetime = end_time - start_time

        if self.to_statistics:
            try:
                stats_info = self.get_scraping_stats_info(action_execution_datetime)
                LoadScrapingStatisticsToDatabase(stats_info).load_to_db()
            except Exception as e:
                logging.warning(f"Populating ScrapingStatistics table failed: {e}\n Tracking: {traceback.format_exc()}")


    def save_data_to_csv(self, item) -> None:
        """Saving data to csv file."""
        try:
            header = False
            if not os.path.exists('scraped.csv'):
                header = True
                df = pd.DataFrame([item], columns=CSV_COLUMNS)
                df.to_csv('scraped.csv', header=header, index=False, mode='a')
            else:
                header = False
                df_e = pd.read_csv('scraped.csv')
                df = pd.DataFrame([item], columns=CSV_COLUMNS)
                if df['item_id'][0] not in df_e['item_id'].tolist():
                    df.to_csv('scraped.csv', header=header, index=False, mode='a')
        except Exception as e:
            logging.warning(f"Saving data to csv failed: {e}\n Tracking: {traceback.format_exc()}")


    def get_scraping_stats_info(self, action_execution_datetime: datetime) -> List[Union[str, int, bool, float]]:
        """Getting scraping stats info."""
        stats_info = list()

        category_type = self.category_type
        start_page = self.start_page
        retrieved_articles_quantity = self.articles_to_retrieve
        time_of_the_action = datetime.utcnow().replace(tzinfo=timezone.utc)
        action_execution_datetime = action_execution_datetime
        searched_article = self.searched_article
        to_csv = self.to_csv
        to_database  = self.to_database
        scrap_continuously = self.scrap_continuously
        scrap_choosen_data = self.scrap_choosen_data

        stats=[category_type, start_page, retrieved_articles_quantity,
            time_of_the_action, action_execution_datetime, searched_article,
            to_csv, to_database, scrap_continuously, scrap_choosen_data]

        for field in stats:
            stats_info.append(field)

        return stats_info


    def scrap_continuously_by_refreshing_page(self) -> List[str]:
        """Scraping data function for continuously scraping feature."""
        retrived_articles = list()

        soup = self.scrap_page()
        time.sleep(20)
        articles = soup.find_all('article')
        retrived_articles += articles

        return retrived_articles


class CheckConditions:


    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup


    def check_if_last_page_nowe(self) -> bool:
        """Checking 'nowe' category to verify if the scraped page is the last one."""
        try:
            searched_ending_string = self.soup.find_all('h1', {"class":"size--all-xl size--fromW3-xxl text--b space--b-2"})[0].get_text()
            if searched_ending_string.startswith("Ups"):
                logging.warning("No more pages to scrap.")
                return False
        except:
            return True

    def check_if_last_page_search(self) -> bool:
        """Checking 'search' category to verify if the scraped page is the last one."""
        try:
            searched_ending_string = self.soup.find_all('h3', {"class":"size--all-l"})[0].get_text()
            searched_articles_number = self.soup.find_all('span', {"class":"box--all-i size--all-s vAlign--all-m"})[0].get_text()
            searched_articles_number = int(searched_articles_number.replace(" ","").strip("\n\t Okazje()"))
            if searched_ending_string.startswith("Ups") and searched_articles_number > 0:
                logging.warning("No more pages to scrap.")
                return False
        except:
            return True

    def check_if_no_items_found(self) -> bool:
        """Checking if searched item was found."""
        try:
            searched_ending_string = self.soup.find_all('h3', {"class":"size--all-l"})[0].get_text()
            searched_articles_number = self.soup.find_all('span', {"class":"box--all-i size--all-s vAlign--all-m"})[0].get_text()
            searched_articles_number = int(searched_articles_number.replace(" ","").strip("\n\t Okazje()"))
            if searched_ending_string.startswith("Ups") and searched_articles_number == 0:
                logging.warning("The searched item was not found.")
                return False
        except:
            return True


"""
category_type = "nowe"
start_page = 2
searched_article = "fsdfsdfsdf"
articles_to_retrieve = 120
to_csv = True
to_database = True
to_statistics = True
scrap_continuously = False
scrap_choosen_data = True
output = ScrapPage(category_type, articles_to_retrieve, to_csv,
                        to_database, to_statistics, start_page, searched_article, scrap_continuously, scrap_choosen_data)

output.select_url()
output.get_items_details_depending_on_the_function()
"""