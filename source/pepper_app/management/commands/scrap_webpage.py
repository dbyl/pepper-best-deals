from requests.exceptions import ConnectionError, HTTPError, MissingSchema, ReadTimeout
import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from enum import Enum, IntEnum
from collections import Counter
import os
from get_info import GetItemAddedDate, GetItemDiscountPrice, GetItemId, GetItemName, GetItemPercentageDiscount, GetItemRegularPrice, GetItemUrl
import csv



from typing import List, Union
import logging
import html5lib


#from populate_database import LoadDataFromCsv, LoadDataFromCsv




class ScrapWebpage:

    def __init__(self, website_url: str, action_type: str, articles_to_retrieve: int,
                to_csv: bool = False, to_database: bool = True, start_page: int = 1) -> None:
        self.website_url = website_url
        self.action_type = action_type
        self.articles_to_retrieve = articles_to_retrieve
        self.to_database = to_database
        self.to_csv = to_csv
        self.start_page = start_page


    def scrap_data(self) -> str:
        try:
            url_to_scrap = self.website_url + self.action_type + str(self.start_page)

            driver = webdriver.Chrome()
            driver.set_window_size(1400,1000)
            driver.get(url_to_scrap)
            time.sleep(0.7)
            page = driver.page_source
            soup = BeautifulSoup(page, 'html5lib')
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



    def get_items_details(self) -> List[Union[str, float, int]]:

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

        return all_items

        """ if to_csv == True:
                self.save_data_to_csv_1()

            if to_pepperarticles_database == True:
                LoadItemDetailesToDatabase.load_to_db(article)"""



    """def save_data_to_csv_1(self) -> None:
        with open('scraped_data.csv', 'a', encoding='UTF8') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            writer.writerow(header)

            with open('scraped_data.csv', 'r', encoding='UTF8', newline='') as read_file:
                csv_reader = csv.reader(read_file)
                existing_rows = list(csv_reader)
                if row not in existing_rows:
                    csv_writer.writerow(row)
                    logging.info("Row appended successfully.")
                else:
                    logging.info("Row already exists in the file.")"""

    def save_data_to_csv(self) -> None:

        header = ['item_id', 'name', 'discount_price', 'percentage_discount', 'regular_price', 'date_added', 'url']
        data = self.get_items_details()

        with open('scraped_data.csv', 'w', encoding='UTF8') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)

            writer.writerow(header)
            writer.writerows(data)



action_type = "/nowe?page="
start_page = 1
website_url = "https://www.pepper.pl"
articles_to_retrieve = 50
to_csv = False
to_database = True
output = ScrapWebpage(website_url, action_type, articles_to_retrieve, to_csv, to_database, start_page)
output.save_data_to_csv()