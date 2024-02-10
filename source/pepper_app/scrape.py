import os
import time
import logging
import pandas as pd
import traceback
from datetime import datetime, timezone
from typing import List, Union
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, HTTPError, MissingSchema, ReadTimeout
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pepper_app.get_info import (GetItemAddedDate,
                                GetItemDiscountPrice,
                                GetItemId,
                                GetItemName,
                                GetItemPercentageDiscount,
                                GetItemRegularPrice,
                                GetItemUrl)
from pepper_app.populate_database import (LoadItemDetailsToDatabase,
                                        LoadScrapingStatisticsToDatabase)
from pepper_app.environment_config import CustomEnvironment
from pepper_app.constans import (CSV_COLUMNS)


class ScrapePage:

    def __init__(self, category_type: str, articles_to_retrieve: int, to_csv: bool=False,
                to_database: bool=True, to_statistics: bool=True, searched_article: str='NA', 
                scrape_continuously: bool=False, scrape_choosen_data: bool=True) -> None:
        self.category_type = category_type
        self.articles_to_retrieve = articles_to_retrieve
        self.to_database = to_database
        self.to_csv = to_csv
        self.to_statistics = to_statistics
        self.start_page = 1
        self.searched_article = searched_article
        self.scrape_continuously = scrape_continuously
        self.scrape_choosen_data = scrape_choosen_data

    def scrape_page(self, url_to_scrape: str, driver: webdriver=None) -> BeautifulSoup:
        """Setting up selenium webdriver, scraping page with bs4."""
        try:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            if driver is None:
                driver = webdriver.Chrome(options=options) #for local  
                #driver = webdriver.Remote(command_executor=f'http://{CustomEnvironment.get_selenium_container_name()}:4444/wd/hub', options=options) #for docker 
            driver.set_window_size(1400,1000)
            driver.get(url_to_scrape)
            time.sleep(0.7)
            page = driver.page_source
            driver.quit()
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
        """Selection of the website address depending on the type of scraping."""
        if self.scrape_continuously == True:
            url_to_scrape = "".join([CustomEnvironment.get_url(), "nowe"])
            return url_to_scrape
        elif self.category_type == "nowe" and self.scrape_continuously == False:
            url_to_scrape = "".join([CustomEnvironment.get_url(), self.category_type, "?page=", str(self.start_page)])
            return url_to_scrape
        elif self.category_type == "search" and self.scrape_continuously == False:
            searched_article = str(self.searched_article.replace(" ","%20"))
            url_to_scrape = "".join([CustomEnvironment.get_url(), self.category_type, "?q=",
                                    searched_article, "&page=", str(self.start_page)])
            return url_to_scrape
        else:
            raise Exception(f"The variables were defined incorrectly.")

    def infinite_scroll_handling(self) -> List[str]:
        """Handling scraping through subsequent pages."""
        try:
            flag = True
            retrived_articles = list()
            while flag:
                url_to_scrape = self.select_url()
                soup = self.scrape_page(url_to_scrape)
                flag_nowe = CheckConditions(soup).check_if_last_page_nowe()
                flag_search = CheckConditions(soup).check_if_last_page_search()

                if flag_nowe == False or flag_search == False:
                    flag = False
                flag = CheckConditions(soup).check_if_no_items_found()

                articles = soup.find_all('article')
                retrived_articles += articles

                if len(retrived_articles) >= self.articles_to_retrieve:
                    flag = False
                else:
                    if self.scrape_continuously == True:
                        time.sleep(10)
                    else:
                        self.start_page += 1
                
                prepared_articles = articles[:self.articles_to_retrieve]
                all_items = self.get_items_details(prepared_articles)
            return all_items
        except Exception as e:
            raise Exception(f"Infinite scroll failed:\
                            {e}\n Tracking: {traceback.format_exc()}")
        

    def get_items_details_depending_on_the_function(self):
        """Completing the list of articles and extracting data details depending on the type of scraping."""
        if self.scrape_continuously == True and self.scrape_choosen_data == False:
            while True:
                all_items = self.infinite_scroll_handling()
                return all_items
        elif self.scrape_continuously == False and self.scrape_choosen_data == True:
            all_items = self.infinite_scroll_handling()
            return all_items
        else:
            raise Exception(f"Matching get_items_details depending on the selected \
                            functionality failed. \n Tracking: {traceback.format_exc()}")
        
    
    def get_items_details(self, prepared_articles):
        """Getting item detailes."""
        start_time = datetime.utcnow().replace(tzinfo=timezone.utc)
        all_items = list()
        try:
            for article in prepared_articles:
                item = list()
                item.extend([GetItemId(article).get_data(), 
                            GetItemName(article).get_data(),
                            GetItemDiscountPrice(article).get_data(),
                            GetItemPercentageDiscount(article).get_data(),
                            GetItemRegularPrice(article).get_data(),
                            GetItemAddedDate(article).get_data(),
                            GetItemUrl(article).get_data()])
                if item not in all_items:
                    all_items.append(item)
                if '' in item:
                    logging.warning("Data retrieving failed. None values detected")
                    break
                if self.to_csv:
                    self.save_data_to_csv(item)
                if self.to_database:
                    LoadItemDetailsToDatabase(item).load_to_db()
                    if self.scrape_continuously == True:
                        pass
                
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
        return all_items

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
        retrieved_articles_quantity = self.articles_to_retrieve
        time_of_the_action = datetime.utcnow().replace(tzinfo=timezone.utc)
        action_execution_datetime = action_execution_datetime
        searched_article = self.searched_article
        to_csv = self.to_csv
        to_database  = self.to_database
        scrape_continuously = self.scrape_continuously
        scrape_choosen_data = self.scrape_choosen_data

        stats=[category_type, retrieved_articles_quantity,
            time_of_the_action, action_execution_datetime, searched_article,
            to_csv, to_database, scrape_continuously, scrape_choosen_data]

        for field in stats:
            stats_info.append(field)

        return stats_info
    

class CheckConditions:

    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    def check_if_last_page_nowe(self) -> bool:
        """Checking 'nowe' category to verify if the scraped page is the last one."""
        try:
            searched_ending_string = self.soup.find_all('h1', {"class":"size--all-xl size--fromW3-xxl text--b space--b-2"})[0].get_text()
            if searched_ending_string.startswith("Ups"):
                logging.warning("No more pages to scrape.")
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
                logging.warning("No more pages to scrape.")
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
        


